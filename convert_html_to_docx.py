#! /usr/bin/env python3
"""
Convert html files to docx using pandoc.
Convert internal .html URLs to .docx.
Leave external .html URLs as is.

Always make a copy of the directory of source files before running this script.
The internal URLs of the .html files will be edited and the files overwritten.
"""

from pathlib import Path
import time

import datasense as ds
import pypandoc


def main():
    header_title = "Convert html files to docx files"
    title_ask_directory = "Directory of html files?"
    header_id = "convert-html-files-to-docx-files"
    output_url = "convert_html_to_docx.html"
    pattern_in_line = "job_aid_"
    new_extension = ".docx"
    old_extension = ".html"
    patterns = [".html"]
    original_stdout = ds.html_begin(
        output_url=output_url, header_title=header_title, header_id=header_id
    )
    ds.script_summary(script_path=Path(__file__), action="started at")
    path_html_files = ds.ask_directory_path(
        title=title_ask_directory, print_bool=True
    )
    start_time = time.perf_counter()
    html_files = ds.list_files(
        directory=path_html_files, patterns=patterns
    )
    html_files = [
        x for x in html_files if x.stem.startswith(pattern_in_line)
    ]
    print(html_files)
    print()
    for f in html_files:
        fr = open(f, "r")
        t = fr.readlines()
        fw = open(f, "w")
        for line in t:
            if pattern_in_line in line and old_extension in line:
                line = line.replace(old_extension, new_extension)
                fw.write(line)
            else:
                fw.write(line)
    for f in html_files:
        pypandoc.convert_file(
            source_file=str(f),
            to="docx",
            format="html",
            outputfile=str(f.with_suffix(new_extension)),
        )
    stop_time = time.perf_counter()
    ds.script_summary(script_path=Path(__file__), action="finished at")
    ds.report_summary(start_time=start_time, stop_time=stop_time)
    ds.html_end(original_stdout=original_stdout, output_url=output_url)


if __name__ == "__main__":
    main()
