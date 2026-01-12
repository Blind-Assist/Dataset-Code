#!/usr/bin/env python3
"""
fix_json_objects.py

Reads an input file that contains multiple top-level JSON objects concatenated together
(or separated by newlines) and writes a single valid JSON array to output.

Usage:
    python fix_json_objects.py input_file.json output_file.json

Behavior:
- Works with objects that span multiple lines.
- Correctly handles braces inside strings and escaped quotes.
- Streams output (doesn't require loading the entire file into memory).
"""
import sys
import json

def iter_json_objects_from_file(path, chunk_size=64*1024):
    """
    Yields complete JSON object strings from a file containing concatenated JSON objects.
    Uses brace-depth tracking and string/escape handling to ignore braces inside strings.
    """
    buf = []
    depth = 0
    in_string = False
    escape = False
    started = False  # whether we've seen the first non-whitespace for current object

    with open(path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            for ch in chunk:
                if not started:
                    if ch.isspace():
                        continue
                    # If we encounter starting '[' then assume file is already a JSON array
                    if ch == '[':
                        # yield special signal: file is array -> stop and let caller handle copying/parse
                        yield ('__FILE_IS_ARRAY__', None)
                        return
                    if ch == '{':
                        started = True
                        depth = 1
                        buf.append(ch)
                        in_string = False
                        escape = False
                        continue
                    # if other chars (like BOM or comments) skip until '{'
                    else:
                        # skip until a starting '{' is found
                        continue
                else:
                    buf.append(ch)
                    if escape:
                        escape = False
                        continue
                    if ch == '\\':
                        escape = True
                        continue
                    if ch == '"':
                        in_string = not in_string
                        continue
                    if in_string:
                        continue
                    if ch == '{':
                        depth += 1
                        continue
                    if ch == '}':
                        depth -= 1
                        if depth == 0:
                            # complete object
                            obj_str = ''.join(buf).strip()
                            if obj_str:
                                yield ('__OBJ__', obj_str)
                            buf = []
                            started = False
                            in_string = False
                            escape = False
                        continue
                    # other characters outside strings ignored for structure purposes
        # end reading file
    # If there's leftover buffer that didn't close properly, try to yield if non-empty
    if buf:
        maybe = ''.join(buf).strip()
        if maybe:
            # attempt a final yield; caller will try to json.loads and may fail if malformed
            yield ('__OBJ__', maybe)

def convert_to_array_streaming(inpath, outpath):
    first = True
    with open(outpath, 'w', encoding='utf-8') as outf:
        outf.write('[')
        for tag, payload in iter_json_objects_from_file(inpath):
            if tag == '__FILE_IS_ARRAY__':
                # If file already contains a JSON array, attempt to parse and pretty-write it
                # Simpler approach: load whole file and re-dump (safe for typical sizes).
                with open(inpath, 'r', encoding='utf-8') as inf:
                    data = json.load(inf)
                json.dump(data, outf, ensure_ascii=False, indent=2)
                outf.write(']')
                return
            elif tag == '__OBJ__':
                try:
                    obj = json.loads(payload)
                except Exception as e:
                    # If it fails, try a safer fallback: strip trailing commas or whitespace and retry
                    cleaned = payload.strip().rstrip(',')
                    try:
                        obj = json.loads(cleaned)
                    except Exception as e2:
                        print(f"Warning: could not parse an object. Skipping. Error: {e2}", file=sys.stderr)
                        continue
                if not first:
                    outf.write(',\n')
                json.dump(obj, outf, ensure_ascii=False, indent=2)
                first = False
        outf.write(']')

def main():
    if len(sys.argv) != 3:
        print("Usage: python fix_json_objects.py input_file.json output_file.json")
        sys.exit(2)
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    convert_to_array_streaming(inpath, outpath)
    print(f"Converted -> {outpath}")

if __name__ == '__main__':
    main()
