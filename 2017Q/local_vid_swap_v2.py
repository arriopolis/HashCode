from check_sol_v2 import read_input
from check_sol_v2 import read_output
from check_sol_v2 import calc_score

if __name__ == "__main__":
    import sys
    import os
    if len(sys.argv) < 3:
        print("Supply the input filename and the submission filename as command line arguments.")
        sys.exit()
    V,E,R,C,X,vidsize,endpoints,requests = read_input(sys.argv[1])
    S,caches = read_output(sys.argv[2])

    vids_requests = {}
    for vid,end,n in requests:
        if vid in vids_requests:
            vids_requests[vid] += n
        else:
            vids_requests[vid] = n

    vids_requests = dict(sorted(vids_requests.items(), key=lambda item: item[1]))
    vids = list(vids_requests)
    score = calc_score(caches, vidsize, endpoints, requests, V, X)

    count = 0
    vid_in_idx = 0
    vid_out_idx = len(vids)-1
    for vid_in_idx in range(len(vids)):
        for vid_out_idx in range(len(vids)):
            vid_in = vids[vid_in_idx]
            vid_out = vids[vid_out_idx]
            if vid_in == vid_out:
                continue

            for i in range(len(caches)):
                size = 0
                for vid in caches[i]:
                    size += vidsize[vid]

                if vid_out in caches[i][1:] and vid_in not in caches[i][1:]:
                    # Check cache size limit
                    if size - vidsize[vid_out] + vidsize[vid_in] > X:
                        break
                    
                    # Update score
                    print('test')
                    score = calc_score(caches, vidsize, endpoints, requests, V, X)
                    
                    caches[i].reverse()
                    caches[i].remove(vid_out)
                    caches[i].reverse()
                    caches[i].append(vid_in)

                    score_new = calc_score(caches, vidsize, endpoints, requests, V, X)

                    # Check if improved
                    if score_new < score:
                        caches[i].reverse()
                        caches[i].remove(vid_in)
                        caches[i].reverse()
                        caches[i].append(vid_out)  
                    else:
                        print("New score:", score_new)
                        file_name = os.path.join(sys.argv[2][:-11]) + "_" + str(calc_score(caches, vidsize, endpoints, requests, V, X)) + '.out'
                        with open(file_name, 'w') as f:
                            f.write(str(len(caches)) + "\n")
                            for c_id, videos in enumerate(caches):
                                if len(caches[c_id]) > 1:
                                    f.write(f"{videos[0]} {' '.join(map(str, videos[1:]))}" + "\n")

            if count%2 == 0:
                vid_in_idx += 1
            else:
                vid_out_idx -= 1

            if vid_out_idx < 0 or vid_in_idx >= len(vids):
                break

            count += 1






    




        