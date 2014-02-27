#!/usr/bin/python
# encoding: utf-8

import subprocess
import re
import json
import unittest


class Regexps:
    dashes = re.compile("^[- ]+$")


def string_partition(s, partitions, delta):
    output = []
    pos = partitions[0] - delta
    for i in xrange(len(partitions) - 1):
        start = pos + delta
        pos = start + partitions[i + 1]
        output.append(s[start:pos].strip())
    return output

def parse_wit_output(wit_output):
    if isinstance(wit_output, str):
        wit_output = wit_output.decode("utf-8")

    if isinstance(wit_output, unicode):
        wit_output = wit_output.splitlines()

    title_row = None
    column_widths = None
    titles = None

    result = []

    for line in wit_output:
        if line.startswith("Query"):
            continue
        if not line.strip():
            continue
        if not title_row:
            title_row = line
            continue
        if title_row and Regexps.dashes.match(line.strip()):
            dashes = line
            initial_whitespace = dashes.index("-")
            column_widths = [initial_whitespace]
            column_widths += map(len, dashes.split())

            titles = [s.strip().lower() for s in
                      string_partition(title_row, column_widths, 1)]
            continue

        if not column_widths:
            raise Exception("Could not parse WIT output, missing dashes line")
        fields = string_partition(line, column_widths, 1)
        workitem = dict(zip(titles, fields))
        result.append(workitem)

    return result


def run_query(collection, project, query):
    p = subprocess.Popen(["false"])
    p.communicate()

    cmd = ["wit", "query", "-collection:%s" % collection,
           "-project:%s" % project, query]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    out, err = p.communicate()

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, cmd)

    return out


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--collection', required=True,
                        help="Collection URL. "
                        "Example: http://server:8080/tfs/DefaultCollection")
    parser.add_argument('--project', required=True, help="Project name")
    parser.add_argument('query', help="Query name")

    args = parser.parse_args()

    output = run_query(args.collection, args.project, args.query)

    print json.dumps(parse_wit_output(output), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()


class JwitTest(unittest.TestCase):
    def testStringPartition(self):
        partitions = [2, 9, 17]
        #      Name       Job
        #      ---------  -----------------
        s = "  John Doe   Financial Analyst"

        self.assertEqual(["John Doe", "Financial Analyst"],
                         string_partition(s, partitions, 2))

    def testParseWitOutput(self):
        example_output = """Query Results: 2 results found for query "X"

  ID     Assigned To      Title
  ------ ---------------- ------------------------------------------------
  123456 Some poor shmuck Things don't "work", generally speaking
  123457 Someone else     Things are generally bad and there are many bugs"""

        expected_result = [
            {
                u"id": u"123456",
                u"assigned to": u"Some poor shmuck",
                u"title": u"Things don't \"work\", generally speaking",
            },
            {
                u"id": u"123457",
                u"assigned to": u"Someone else",
                u"title": u"Things are generally bad and there are many bugs",
            },
        ]

        self.assertEqual(expected_result, parse_wit_output(example_output))
