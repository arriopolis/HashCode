import sys
from read_input import Instance


class Solution:
    def __init__(self):
        self.ready_time_of_file_at_server = []
        self.E = []
        self.compilation_steps = []

    def readfile(self, filepath):
        f = open(filepath, 'r')
        self.E = int(f.readline())
        for _ in range(self.E):
            name, s = f.readline().split()
            self.compilation_steps.append((name, int(s)))

    def determine_score(self, instance):
        self.ready_time_of_file_at_server = [dict() for server in range(instance.S)]
        server_time = [0 for server in range(instance.S)]
        for step in self.compilation_steps:
            name, server = step[0], step[1]
            _, c, r = [file for file in instance.compiled_files if file[0] == name][0]
            ready_time_of_latest_dependency = 0
            if instance.dependencies_dict[name]:
                ready_time_of_latest_dependency = max([self.ready_time_of_file_at_server[server][dependency] for dependency in instance.dependencies_dict[name]])
            server_time[server] = max(ready_time_of_latest_dependency, server_time[server]) + c
            self.ready_time_of_file_at_server[server][name] = server_time[server]
            for other_server in range(instance.S):
                if other_server != server:
                    time_after_replication = server_time[server] + r
                    if name not in self.ready_time_of_file_at_server[other_server].keys() or time_after_replication < self.ready_time_of_file_at_server[other_server][name]:
                        self.ready_time_of_file_at_server[other_server][name] = time_after_replication
        for server in range(instance.S):
            print(self.ready_time_of_file_at_server[server])
        score = 0
        for name, target in instance.target_files_dict.items():
            deadline, goal_points = target[0], target[1]
            ready_times_of_target_at_servers = [self.ready_time_of_file_at_server[server][name] for server in range(instance.S) if name in self.ready_time_of_file_at_server[server].keys()]
            if ready_times_of_target_at_servers:
                time = min(ready_times_of_target_at_servers)
                if time < deadline + 1:
                    score += deadline - time + goal_points
        return score


def main():
    solution = Solution()
    solution.readfile(sys.argv[2])
    # print(solution.E)
    # for e in range(solution.E):
    #     print(solution.compilation_steps[e])
    instance = Instance(sys.argv[1])
    print(solution.determine_score(instance))


if __name__ == '__main__':
    main()