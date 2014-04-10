#!/usr/bin/python

import argparse
import static_scan
import fuzz

if __name__ == "__main__":
    """Main method

    """
    parser = argparse.ArgumentParser(description='Static php source scan and fuzz')
    parser.add_argument('-d', '--directory', action="store", dest="folder", required=True, help='Base folder')
    parser.add_argument('-f', '--fuzz', action="store_true", dest="fuzz", default=False, help='Base folder')
    parser.add_argument('-o', '--output', action="store", dest="output", default="pretty", help='Output type (pretty or json)')
    parser.add_argument('-c', '--cookies', action="store", dest="cookies", default=None, help='Cookies')
    parser.add_argument('-n', '--nbtests', action="store", default=1, dest="nb_tests", help='Nb test per entrypoint')
    parser.add_argument('-u', '--url', action="store", dest="url", help='Url matching folder value')
    parser.add_argument('-r', '--recursive', action="store_true", dest="recursive", default=False, help='Recursive file search')
    parser.add_argument('-l', '--logfile', action="store", dest="log_file", default=None, help='Log file to watch')
    args = parser.parse_args()

    # Start entry points scan
    if args.output == "pretty":
        print "[*] Starting static scan"
    sps = static_scan.StaticPhpScanner(args.folder, args.recursive)
    entry_points = sps.scan(args.output)

    # display entry points
    if not args.fuzz:
        if args.output == "pretty":
            for url, vars in entry_points.items():
                print "[+] %s" % url
                for action in vars:
                    print " | [%s] line %d : %s" % (action['method'], action['line'], action['var'])
        elif args.output == "json":
            print entry_points

    # Perform fuzzing
    if args.fuzz:
        fuzzer = fuzz.Fuzzer(args.url, args.log_file, args.cookies)
        if args.output == "pretty":
            print "[*] Starting fuzz"
        results = fuzzer.fuzz(args.folder, entry_points, args.nb_tests, args.output)

        # Display a pretty graph
        if args.output == "pretty":
            for result in results:
                for url, datas in result.items():
                    for data in datas:
                        print "[+] %s %s : %s" % (data['response'], data['method'], url)
                        print " |"
                        for param, value in data['data'].items():
                            print " | %s : 0x%s" % (param, value.encode('hex'))
                        if len(data['informations']) > 0:
                            print " |\r\n" + " |- logs :\r\n" + " |"
                            for log in data['informations']:
                                print " | %s" % log
                        print ""
        elif args.output == "json":
            print results
