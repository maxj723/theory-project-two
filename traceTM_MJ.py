import argparse
import csv

class NTM:
    def __init__(self, name, Q, sigma, gamma, start, accept, reject, transitions):
        self.name = name
        self.Q = Q
        self.sigma = sigma
        self.gamma = gamma
        self.start = start
        self.accept = accept
        self.reject = reject

        self.transitions = transitions

    # Run transitions on input config and determine next possible configs
    def get_next_config(self, cfg):
        left, state, right = cfg

        # Determine symbol under head (_ if blank)
        if right == '':
            symbol = '_'
        else:
            symbol = right[0]

        # If state and symbol are transitionable, find next configs
        if state in self.transitions and symbol in self.transitions[state]:
            next_cfgs = []
            # Iterate through all possible transitions
            for t in self.transitions[state][symbol]:
                next_state = t['next_state']
                write_symbol = t['write_symbol']
                direction = t['direction']

                new_left = left
                new_right = right

                # If at the end of tape, write the symbol, else replace old
                if new_right == '':
                    new_right = write_symbol
                else:
                    new_right = write_symbol + right[1:]

                # If R, shift tape and adjust left/right
                if direction == 'R':
                    new_left += new_right[0]
                    new_right = new_right[1:]
                # If L, shift tape and adjust left/right
                else:
                    # If at the beginning of the tape, reject bc can't move more left
                    if len(new_left) == 0:
                        new_left = left
                        new_right = right
                        next_state = self.reject
                    else:
                        new_right = new_left[-1] + new_right
                        new_left = new_left[:-1]

                # add new config
                next_cfgs.append([new_left, next_state, new_right])
            return next_cfgs
        
        else:
            return [[left, self.reject, right]]

    # Given input string, Run TM and accept/reject. Print Output
    def process_input(self, input_string, max_depth):

        # Initialize tree with only start and total transitions to 0
        tree = []
        start_config = ["", self.start, input_string]
        tree.append([start_config])
        num_configs = 0

        # Initialize status variables to identify exit
        accept_found = False
        all_reject = True
        max_depth_occurred = False

        # Run BFS on tree, exiting when tree no longer has levels to explore
        current_level = 0
        while current_level < len(tree):

            # Check for max depth exit
            if current_level > max_depth:
                max_depth_occurred = True
                all_reject = False
                break

            # Iterate through configs in current level
            current_configs = tree[current_level]  
            next_configs = []  
            for cfg in current_configs:
                _, state, _ = cfg

                # Check for accept exit
                if state == self.accept:
                    accept_found = True
                    all_reject = False
                    break

                # If reject, skip
                if state == self.reject:
                    continue
                
                # Find next possible configs for given config, and add to next level
                next_configs += (self.get_next_config(cfg))

            # if not accepted yet, update total transitions and tree
            if not accept_found:
                num_configs += len(next_configs)

                if len(next_configs) > 0:
                    tree.append(next_configs)

            # Move to next level
            current_level += 1
        
        # Move back a level due to unneccessary add at the end
        current_level -= 1

        # Print output in desired format
        self.print_output(accept_found, all_reject, max_depth_occurred, max_depth, current_level, num_configs, tree)

    # function to print the output as required
    def print_output(self, accept, reject, max_depth_occurred, max_depth, level, total_trans, tree):
        
        print(f'Depth: {level}')
        print(f'Total transitions: {total_trans}')

        if accept:
            print(f'String accepted in {level}')
            for level in tree:
               print(level)

        if reject:
            print(f'String rejected in {level}')
            
        if max_depth_occurred:
            print(f'Execution stopped after {max_depth}')

# Convert CSV file to NTM object    
def process_csv(csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)

        # Process the first 7 lines of the file
        name = next(csv_reader)[0]
        Q = next(csv_reader)
        sigma = next(csv_reader)
        gamma = next(csv_reader)
        start = next(csv_reader)[0]
        accept = next(csv_reader)[0]
        reject = next(csv_reader)[0]

        # Process transition function as dictionary
        transitions = {}
        for line in csv_reader:
            current_state, read_symbol, next_state, write_symbol, direction = line

            if current_state not in transitions:
                transitions[current_state] = {}
            if read_symbol not in transitions[current_state]:
                transitions[current_state][read_symbol] = []
            
            transitions[current_state][read_symbol].append({
                'next_state': next_state,
                'write_symbol': write_symbol,
                'direction': direction
            })
        # Format will look like this:
        # {
        #     'q1': {
        #         'a': [
        #             {'next_state': 'q1', 'write_symbol': 'a', 'direction': 'R'},
        #             {'next_state': 'q2', 'write_symbol': 'a', 'direction': 'R'}
        #         ]
        #     },
        #     'q2': {
        #         '_': [
        #             {'next_state': 'q3', 'write_symbol': '_', 'direction': 'L'}
        #         ]
        #     }
        # }
    
    ntm = NTM(name, Q, sigma, gamma, start, accept, reject, transitions)
    return ntm


def __main__():

    # parse cmd line args
    parser = argparse.ArgumentParser()
    parser.add_argument('NTM_file', type=str)
    parser.add_argument('input_string', type=str)
    parser.add_argument('max_depth', type=int)
    args = parser.parse_args()

    # Convert csv to NTM 
    NTM = process_csv(args.NTM_file)

    print(NTM.name)
    print(f'Input string: {args.input_string}')

    # Run input on NTM
    NTM.process_input(args.input_string, args.max_depth)

if __name__ == '__main__':
    __main__()