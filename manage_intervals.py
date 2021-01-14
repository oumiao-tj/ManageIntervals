from bisect import bisect_left

class ManageIntervals():
    def __init__(self):
        # initial state is an empty array
        # self.res is always updated to be sorted in start time
        self.res = []
        
    def add(self, start, end):
        # deal with some edge cases
        if start == end:
            return self.res
        if start > end:
            raise ValueError("Start time is larger than the end time!")
        if not self.res:
            self.res.append((start, end))
            return self.res
        
        n = len(self.res)
        all_starts = [x[0] for x in self.res]
        idx = bisect_left(all_starts, start) # idx is the place to insert start into all sorted starts
        # take care of the case where there is no overlapping
        if (idx == 0 or self.res[idx - 1][1] < start) and (idx == n or self.res[idx][0] > end):
            self.res.insert(idx, (start, end))
            return self.res
        # Otherwise, there must be overlapping between some old intervals with the new interval (start, end)
        i = max(idx - 1, 0)
        first_overlap = None
        while i < n:
            # capture the index of the first overlapping interval
            if first_overlap == None and self.overlap(self.res[i], (start, end)):
                first_overlap = i
            # when it stops overlapping, break the loop, because no further intervals will have overlap
            elif first_overlap != None and self.overlap(self.res[i], (start, end)) == False:
                break
            i += 1
            
        self.res = self.res[:first_overlap] + [(min(self.res[first_overlap][0], start),\
                                                max(self.res[i-1][1], end))] + self.res[i:]
        return self.res
    
    def remove(self, start, end):
        # deal with some edge cases
        if start == end:
            return self.res
        if start > end:
            raise ValueError("Start time is larger than the end time!")
        if not self.res:
            return self.res
        n = len(self.res)
        all_starts = [x[0] for x in self.res]
        idx = bisect_left(all_starts, start) # idx is the place to insert start into all sorted starts
        # take care of the case where there is no overlapping
        if (idx == 0 or self.res[idx - 1][1] < start) and (idx == n or self.res[idx][0] > end):
            return self.res
        
        i = max(idx - 1, 0)
        first_overlap = None
        while i < n:
            # capture the index of the first overlapping interval
            if first_overlap == None and self.overlap(self.res[i], (start, end)):
                first_overlap = i
            # when it stops overlapping, break the loop, because no further intervals will have overlap
            elif first_overlap != None and self.overlap(self.res[i], (start, end)) == False:
                break
            i += 1
        middle_lst = []
        # take care of two intervals near the boundary of removed interval
        if self.res[first_overlap][0] < start:
            middle_lst.append((self.res[first_overlap][0], start))
        if self.res[i-1][1] > end:
            middle_lst.append((end, self.res[i-1][1]))
            
        self.res = self.res[:first_overlap] + middle_lst + self.res[i:]

        return self.res
        
    # determine whether two intervals overlap
    def overlap(self, interval_1, interval_2):
        a1, b1 = interval_1
        a2, b2 = interval_2
        if b1 >= a2 and b2 >= a1:
            return True
        else:
            return False
        
# unit test
if __name__ == "__main__":
    # Initialize a ManageIntervals class
    MI = ManageIntervals()
    
    # generate a list of time intervals and actions
    from random import randint
    intervals = []
    while len(intervals) < 20:
        start = randint(0, 49)
        end = randint(start + 1, 50)
        action = "add" if randint(0, 1) else "remove"
        intervals.append((start, end, action))
    
    # apply the time intervals and actions
    for start, end, action in intervals:
        if action == "add":
            MI.add(start, end)
        else:
            MI.remove(start, end)
        print("{} ({}, {}) => {}".format(action, start, end, MI.res))
