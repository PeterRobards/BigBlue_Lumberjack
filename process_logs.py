#!/usr/bin/env python
"""
    Python Tool designed to process the RAW text Access Logs from a Webhosting provider,
    extracting the following key values: "ip address, date, time, method, url, protocol,
    status, bytes, user_agent, website, and dest_url - which represent the key data points
    contained within the log file
"""
# -*- coding: utf-8 -*-
#
# RAW Access Log Processor -- Version 1.1
# - Peter Robards.
#
##########################################################################################
# Log File Format:
#    IP - - [Date] “REQUEST /url PROTOCOL/1.1” Code# # “-“ “user/agent” website.com websiteIP
#
# Note: This tool is designed process all files in a given directory with the same file extension
#  To set all files in the current working directory to the same extension (i.e. '.log') via bash:
#     for f in *; do mv "$f" "$f.log"; done
##########################################################################################

__author__ = ["Peter Robards"]
__date__ = "02/23/2021"
__description__ = (
    "Reformat and/or Search RAW text Access Logs from BlueHost.com"
)

import os
import re
import sys
import csv
import glob
import json
import argparse

############################### Method Definitions ########################################
def check_path(dir_path):
    """Method to check that provided Directory exists and is valid"""
    if not os.path.exists(dir_path):
        print("\n[!] ERROR -> '{}' is NOT a valid Directory ...\n".format(dir_path))
        print("\n******* ******* *******")
        sys.exit(1)


def validate_ip(line):
    """Method to check that input matches a valid IPv4 address"""
    is_valid = ""
    # RegEx to check for valid IPv4 address below.
    # Note: ^ $ ensure string matche exactly, 25[ ensures 0 - 255 range
    # ^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$
    matched = re.match(
        r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        line,
    )
    if matched:
        # matches a date and adds it to is_valid
        is_valid = matched.group()
    else:
        is_valid = "NONE"
    return is_valid


def get_user_agent(text):
    """Method to extract the user_agent data from the very end of a string surrounded by quotes"""
    matches = re.findall(r"\"(.+?)\"", text)
    # matches is now ['String 1', 'String 2', 'String3']
    if matches:
        user_agent_info = " ".join(str(x) for x in matches[-1:])
    else:
        user_agent_info = ""

    return user_agent_info


def get_date(text):
    """Method to extract the date from right before a colon in a string surrounded by quotes"""
    match = re.search(r"\[(.+?)\]", text)
    if match:
        match_string = match.group()
    else:
        match_string = ""
    # print("{}".format(match_string))
    # match should now be a combination of the date and time, we just want the date portion...
    date_string = match_string.split(":", 1)[0]
    return date_string.strip(r"\[")


def get_time(text):
    """Method to extract the time from right after a colon in a string surrounded by quotes"""
    match = re.search(r"\[.+?\]", text)
    if match:
        match_string = match.group()
    # match_string should now be a combination of the date and time,
    # we just want the time portion...
    time_string = match_string.split(":", 1)[1]
    return time_string.strip(r"\]")


def get_method_url_protocol(text):
    """Method to extract the Request Method, URL, and Protocol in a string surrounded by quotes"""
    match = re.search(r"\".+?\"", text)
    if match:
        match_string = match.group()
    # Note: match should now be a combination of the Request Method, URL, and Protocol...
    # Method should be the first element when dividing the string by spaces
    method_string = match_string.split()[0]
    # URL should be the second element when dividing the string by spaces
    url_string = match_string.split()[1]
    # Protocol should be the final element when dividing the string by spaces
    protocol_string = match_string.split()[-1]
    return method_string.strip('"'), url_string, protocol_string.strip('"')


def get_website(text):
    """Extracts the website which should be the penultimate value in a string split on spaces"""
    strings = text.split()
    # strings should now have all the items in our line separated by spaces,
    # we want the penultimate one..
    website_string = strings[len(strings) - 2]
    return website_string


def get_search_params(log_list):
    """Ask user to input and then return a series of  search parameters relating to the log file"""
    key_values = log_list[0].keys()
    not_done = True
    print(
        "\tNote: search parameters consist of valid Key - Value pairs: 'ip':'127.0.0.1' "
    )

    while not_done:
        print("\n[>] Valid Column Names: [{}]".format(", ".join(key_values)))
        input_params = input(
            "\t[->] Please enter the number of parameters (key:value pairs) to search for: "
        )
        if input_params.isdigit():
            num_params = int(input_params)
            if num_params > 1:
                if num_params > len(key_values):
                    print(
                        "\n\t[!] WARNING -> Number of Parameters: '{}' exceeds number of columns!"
                    )
                    print(
                        "\t[+] Setting Number of Parameters to MAX: {}".format(
                            len(key_values)
                        )
                    )
                    num_params = len(key_values)
                param_keys = []
                # Note: Consider validating the input for param_values if using in production
                param_values = []
                for _ in range(num_params):
                    user_input = input(
                        "\n\t[->] Please Enter a key Column to search within: "
                    )
                    if user_input in key_values:
                        param_keys.append(user_input)
                        search_value = input(
                            "\t[->] Please enter some corresponding value to search for: "
                        )
                        param_values.append(search_value)
                    else:
                        print(
                            "\n\t[!] ERROR -> '{}' NOT found in KEYS: {}".format(
                                user_input, key_values
                            )
                        )
                not_done = False
                return param_keys, param_values
            # else:
            user_input = input(
                "\n\t[->] Please Enter a key matching a Column to search within: "
            )
            if user_input in key_values:
                param_key = user_input
                # Note: Consider validating the input for param_value if using in production
                param_value = input(
                    "\t[->] Please enter some corresponding value to search for: "
                )
            else:
                print(
                    "\n\t[!] ERROR -> '{}' NOT found in valid Columns: {}".format(
                        user_input, key_values
                    )
                )
            not_done = False
            return param_key, param_value

        # else:
        print(
            "\n[!] ERROR -> '{}' is NOT a valid positive integer...\n".format(
                input_params
            )
        )


def find_target_events(log_list, search_key, search_value):
    """Return the log events that match the provided search parameters"""

    if isinstance(search_key, list):
        search_string = ""
        first_time = True
        for key, value in zip(search_key, search_value):
            if first_time:
                search_string += 'log_event["{}"] == "{}"'.format(key, value)
                first_time = False
            else:
                search_string += ' and log_event["{}"] == "{}"'.format(key, value)

        print("[+] Searching for :\n\t'{}'".format(search_string))

        # WARNING: the use of eval() below is not super secure, consider validating the variable
        #          created directly above: 'search_string', for potentially malicious input
        #          if deploying to a production environment - 'search_value' is most at risk.
        #          Or possibly implement a different method for handling multiple parameters here.
        # See 'get_search_params()' for where the search_key, search_value inputs are entered
        target_events = list(
            filter(
                lambda log_event: eval(search_string),
                log_list,
            )
        )
    else:
        print(
            '[+] Searching for :\n\t\'log_event["{}"] == "{}"\''.format(
                search_key, search_value
            )
        )
        # Note: In Python 3 a filter object is returned, which is why filter() is wrapped in list()
        target_events = list(
            filter(
                lambda log_event: log_event[search_key] == search_value,
                log_list,
            )
        )

    return target_events


def perform_search(target_list, search_key, search_value):
    """Search Python Dictionary consisting of log events for all matches to given parameters"""
    search_results = []
    search_results += find_target_events(target_list, search_key, search_value)
    return search_results


def process_files(target_files, dir_out, search_for, save_files, export_type):
    """
    Process the specified log files, converting the raw log files to CSV and
    searching them for specific events - if the search option has been selected
    """
    if search_for:
        search_results = []
        first_pass = True

    for file_path in target_files:
        with open(file_path) as file_name:
            print("\n[*] Processing Log File: {}".format(file_name.name))
            with open(file_name.name) as in_file:
                new_list = list(generate_dict(in_file))

                if search_for:
                    if first_pass:
                        print("\n[*] Search Function Selected...")
                        search_key, search_value = get_search_params(new_list)
                        first_pass = False
                    search_results += perform_search(new_list, search_key, search_value)

                # Note: new_list is a list of dictionaries, with each
                #       dictionary representing a single log event.
                # Accessing/Viewing each events can be achieved via index:
                # print("{}\n".format(new_list[0]))
                # print("{}\n".format(new_list[1]))
                # print("{}\n".format(new_list[2]))

                if save_files:
                    just_file_name = file_name.name.rsplit("/")[-1]
                    # Export data to one of the currently supported file types
                    export_data(export_type, new_list, dir_out, just_file_name)

                new_list = []
                print("\n******* ******* *******")

    if search_for:
        return search_results
    return new_list


def generate_dict(log_fh):
    """
    Generates a Python Dictionary from a plain text log file where
    each line is parsed into key/value pairs to better organize the data
    """
    current_dict = {}
    for line in log_fh:
        if line.startswith(validate_ip(line.split()[0])):
            if current_dict:
                yield current_dict
            method, url, protocol = get_method_url_protocol(line)
            current_dict = {
                "ip": line.split()[0],
                "date": get_date(line),
                "time": get_time(line),
                "method": method,
                "url": url,
                "protocol": protocol,
                "status": int(line.split()[8]),
                "bytes": line.split()[9],
                "user_agent": get_user_agent(line),
                "website": get_website(line),
                "dest_url": line.split()[-1],
            }
        else:
            print(
                "\n[!] WARNING --> First line item not a valid IP address, check log file format!"
            )
            print("[!]\tFirst Item : --> {}".format(line.split()[0]))
            current_dict["ip"] += ""
    yield current_dict


def write_to_jsonfile(dict_data, dir_out, out_file):
    """Method to export a list of Python Dictionaries to a JSON file"""

    dir_name = dir_out
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    try:
        with open(os.path.join(dir_name, out_file), "w") as json_file:
            json.dump(dict_data, json_file)
    except IOError:
        print("\n[!] WARNING --> I/O Error!")


def write_to_csvfile(dict_data, dir_out, out_file):
    """Method to export the data in a list of Python Dictionaries to a CSV file"""
    csv_columns = dict_data[0].keys()

    dir_name = dir_out
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    try:
        with open(os.path.join(dir_name, out_file), "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("\n[!] WARNING --> I/O Error!")


def export_data(export_type, dict_data, dir_out, file_name):
    """Method to determine which format the user selected to export data as"""
    if export_type == "CSV":
        out_file = file_name.rsplit(".", 1)[0] + ".csv"
        print("[+] Exporting data to: {}/{}".format(dir_out, out_file))
        write_to_csvfile(dict_data, dir_out, out_file)
    elif export_type == "JSON":
        out_file = file_name.rsplit(".", 1)[0] + ".json"
        print("[+] Exporting data to: {}/{}".format(dir_out, out_file))
        write_to_jsonfile(dict_data, dir_out, out_file)
    else:
        print("\n[!] ERROR -> Export Type: '{}' is NOT valid!".format(export_type))
        print("[-] File(s) FAILED to export...")


################################# Main() Method #########################################
def main():
    """Main() Method"""
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Last Modified by {} on {}".format(", ".join(__author__), __date__),
    )
    parser.add_argument(
        "-i",
        "--input_path",
        nargs="?",
        dest="input_path",
        help="The path to the directory containing the log files you wish to add as input",
    )
    parser.add_argument(
        "-l",
        "--log_files",
        nargs="?",
        dest="log_files",
        help="Signal the file type (via its extension: 'txt', 'log', etc) to target",
    )
    parser.add_argument(
        "-o",
        "--output_results",
        nargs="?",
        dest="output_results",
        default=None,
        help="Output file name where you want to save the results from a search",
    )
    parser.add_argument(
        "-e",
        "--export_type",
        nargs="?",
        dest="export_type",
        choices=["CSV", "JSON"],
        default="CSV",
        help="Signal the type of file in the directory to target (default=CSV)",
    )
    parser.add_argument(
        "-s",
        "--search_for",
        dest="search_for",
        action="store_true",
        help="Signal that you want to search for log events matching a certain pattern",
    )
    parser.add_argument(
        "-S",
        "--save_files",
        dest="save_files",
        action="store_true",
        help="Signal that you wish to save the raw log files to a different format",
    )
    parser.add_argument(
        "-D",
        "--directory_out",
        nargs="?",
        dest="dir_out",
        default="FormattedLogFiles",
        help="Set the name of the Directory to save the converted log files in",
    )

    # Check for above arguments - if none are provided, Display --help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    print("\n*** Running '{}' ***".format(sys.argv[0]))

    search_for = args.search_for
    save_files = args.save_files
    export_type = args.export_type
    dir_out = args.dir_out

    if args.input_path:
        input_dir = args.input_path
    else:
        input_dir = input(
            "\n[->] Enter the name of the directory containing the files you want to process: "
        )
    # Check to make sure the target input Directory actually exists, if not exit and alert user
    check_path(input_dir)
    print("[+] Accessing Input Directory: '{}'".format(input_dir))

    if args.log_files:
        file_ext = args.log_files
    else:
        file_ext = input(
            "\n[->] Enter the extension for the file types you wish to process (e.g. txt, log): "
        )

    if search_for:
        if args.output_results:
            output_results = args.output_results
        else:
            output_results = input(
                "\n[->] Please enter the name of file where you wish to save search results: "
            )

    target_files = glob.glob(os.path.join(input_dir, "*." + file_ext))
    search_results = process_files(
        target_files, dir_out, search_for, save_files, export_type
    )

    if search_for:
        print(
            "\n[*] Saving Search Results to: {}/{}".format(dir_out, output_results)
        )

        # Export search results to one of the currently supported file types
        export_data(export_type, search_results, dir_out, output_results)
        print("\n******* ******* *******")


##########################################################################################

if __name__ == "__main__":

    main()
