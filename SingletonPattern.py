class StatisticsManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StatisticsManager, cls).__new__(cls)
            print("--- New StatisticsManager instance created ---")
        else:
            print("--- Returning existing StatisticsManager instance ---")
        return cls._instance

    def __init__(self, data_list):
        if not hasattr(self, 'data'):
            self.data = data_list
            print(f"Data set to: {self.data}")
    def mean(self):
        if not self.data:
            return 0
        return sum(self.data) / len(self.data)
    def median(self):
        if not self.data:
            return 0
        sorted_list = sorted(self.data)
        n = len(sorted_list)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_list[mid - 1] + sorted_list[mid]) / 2
        else:
            return sorted_list[mid]
    def mode(self):
        if not self.data:
            return 0
        frequency = {}
        for item in self.data:
            frequency[item] = frequency.get(item, 0) + 1     
        if len(frequency) == len(self.data):
            return self.data[0]        
        max_count = max(frequency.values())
        modes = [key for key, count in frequency.items() if count == max_count]
        return modes[0]
def main():
    test_list = [8, 2, 5, 3, 9, 6, 2, 7]
    print(f"List: {test_list}\n")
    print("Attempting to create first manager (s1)...")
    s1 = StatisticsManager(test_list)
    print(f"First manager object s1 address: {id(s1)}")    
    print("\nAttempting to create second manager (s2)...")
    s2 = StatisticsManager([1, 2, 3]) 
    print(f"Second manager object s2 address: {id(s2)}\n")
    print(f"Are s1 and s2 the same object? (s1 is s2): {s1 is s2}\n")
    print("--- Running Calculations using 's1' ---")
    print(f"List in manager: {s1.data}")   
    mode_value = s1.mode()
    print(f"Mode: {mode_value}")    
    median_value = s1.median()
    print(f"Median: {median_value}")    
    mean_value = s1.mean()
    print(f"Mean: {mean_value}")
if __name__ == "__main__":
    main()
