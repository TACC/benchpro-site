
# System imports
import copy
import os
import signal
import sys
import time

class init(object):

    # Catch user interrupt
    def signal_handler(self, sig, frame):

        # Print raw error in dev mode
        if self.glob.dev_mode:
            print(sig)
        # Send to log
        elif self.glob.log:
            self.high('    Writing to log, cleaning up and aborting...')
            self.glob.lib.msg.log("Caught user interrupt, exitting.")
        else:
            print("    Aborting.")

        # Remove files
        self.glob.lib.files.rollback()
        sys.exit(1)

    def __init__(self, glob):
        self.glob = glob
        # Init interrupt handler
        signal.signal(signal.SIGINT, self.signal_handler) 
    
    # Convert strings to lists: str -> [str], list -> list
    def listify(self, message):
        if not isinstance(message, list):
            return [message]
        return message
   
    # Write message to log 
    def log(self, message):
        # If initialized
        if self.glob.log:
            self.glob.log.debug(message)

    # Log and print to stdout
    def log_and_print(self, message, priority):
        message = self.listify(message)

        # For each line of message
        for line in message:
            if line:
                # Write to log 
                self.log(line)
                # Print to stdout if debug=True or high priority message
                if self.glob.stg['debug'] or priority: 
                    print(line)

        # Print line break for multiple 
        if len(message) > 1 and (self.glob.stg['debug'] or priority):
            print()

    # High priority message, nonconditional
    def high(self, message):
        self.log_and_print(message, True)   

    # Low priority message, conditional on debug=True
    def low(self, message):
        self.log_and_print(message, False)            

    # Print message to log and stdout then continue
    def warning(self, message):
        self.log_and_print([self.glob.warning] + self.listify(message), True)

    # Print message to log and stdout then quit
    def error(self, message):
        message = self.listify(message)

        self.log_and_print(["", 
                            ""] + 
                            [self.glob.error] + 
                            self.listify(message) +
                            ["Check log for details."],
                            True)

        # Clean tmp files
        if self.glob.stg['clean_on_fail']:
            self.log_and_print("Cleaning up tmp files...", True)
            self.glob.lib.files.rollback()

        self.log_and_print(["Quitting", ""], True)

        sys.exit(1)

    # Print heading text in bold
    def heading(self, message):
        message = self.listify(message)

        message[0] = self.glob.bold + message[0]
        message[-1] = message[-1] + self.glob.end

        self.log_and_print([""] + message, True)

    # Print section break
    def brk(self):
        print("---------------------------")
        print()


    # Get list of uncaptured results and print note to user
    def new_results(self):

        if not self.glob.stg['skip_result_check']:

            self.log_and_print(["Checking for uncaptured results..."], False)
            # Uncaptured results + job complete
            complete_results = self.glob.lib.get_completed_results(self.glob.lib.get_pending_results(), True)
            if complete_results:
                self.log_and_print([self.glob.note,
                                    "There are " + str(len(complete_results)) + " uncaptured results found in " + 
                                    self.glob.lib.rel_path(self.glob.stg['pending_path']),
                                    "Run 'benchpro --capture' to send to database."], False)
            else:
                self.log_and_print(["No new results found.",
                                    ""], False)


    # Print message about application exe file
    def exe_check(self, exe, search_path):   
        # Check if it exists
        exe_exists = self.glob.lib.files.exists(exe, search_path)

        if exe_exists:
            self.low(["Application executable found in:",
                            ">  " + self.glob.lib.rel_path(search_path)])
        else:
            self.error("failed to locate application executable '" + exe + "'in " + self.glob.lib.rel_path(search_path))

    # Print last 20 lines of file
    def print_file_tail(self, file_path):

        # File exists
        if not os.path.isfile(file_path):
            self.glob.lib.msg.error("File not found: " + self.glob.lib.rel_path(file_path))

        print()
        print("=====> " + self.glob.lib.rel_path(file_path) + " <=====")
        print("...")

        # Print last 20 lines
        with open(file_path, 'r') as fd:
                lines = fd.readlines()
                [print(x.strip()) for x in lines[max(-30, (len(lines)*-1)):]]

        print("=====> " + self.glob.lib.rel_path(file_path) + " <=====")

    # Print the list of installed applications
    def print_app_table(self):

        # Get list of apps 
        apps = self.glob.installed_app_list
        # Reorder columns
        order = [0, 5, 6, 1, 2, 3, 4, 7, 8]

        # Add header row
        apps = [["TASK ID", "SYSTEM", "ARCH", "COMPILER", "MPI", "CODE", "VERSION", "LABEL", "\x1b[0;37mSTATUS\x1b[0m"]] + apps
        cols = len(apps[0])

        # Check header has same num cols and content
        if len(apps[0]) != (len(apps[1])):
            self.glob.lib.msg.error("Mismatched number of table columns.")

        # Get max length of each table column (for spacing)
        padding = [0] * cols
        for i in range(cols):
            for app in apps:
                if len(str(app[i])) > padding[i]:
                    padding[i] = len(str(app[i]))

        # Buffer each column 2 chars
        padding = [i + 2 for i in padding]

        # Print contents
        for idx in range(0,len(apps)): 
            text_col = self.glob.white
            if (idx % 2) == 0:
                text_col = self.glob.grey

            print("| ", end='')
            for column in range(cols):
                print(text_col + str(apps[idx][order[column]]).ljust(padding[order[column]]) + self.glob.end + "| ", end='')
            print()

    # Print timing
    def wait(self, secs):
        for i in range(secs):
            print(".", end='')
            time.sleep(1)
        print()

	# Print random hint
	def print_hint(self):
	"""

	"""

		if self.glob.stg['print_hint']:
		    with open(os.path.join(bp_site, "hints.txt")) as hint_file:
		        hints = hint_file.readlines()

	    	hint = hints[rand(0:len(hints))]
			print(hint)
