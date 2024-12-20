import heapq

class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.patient_count = 0  # This will help break ties when two patients have the same age

    def add_patient(self, name, age):
        # Insert (-age) to prioritize older patients, patient_count ensures stable insertion
        heapq.heappush(self.queue, (age, self.patient_count, name))
        self.patient_count += 1
        self._rebalance_queue()  # Ensure the queue is reordered after insertion

    def _rebalance_queue(self):
        # Sort the queue based on age (the first element of the tuple is -age)
        self.queue.sort(key=lambda x: x[0], reverse=True)  # Ensure descending order of age

    def call_patient(self):
        # Call the patient with the highest priority (oldest) without reordering
        if self.queue:
            # Pop the top of the queue (first element since it is already ordered)
            age, _, patient = self.queue.pop(0)
            print(f"Called patient: {patient}")
            return patient
        return None

    def remove_patient(self, name):
        # Removes a patient by name and rebalances the queue
        self.queue = [patient for patient in self.queue if patient[2] != name]
        heapq.heapify(self.queue)  # Re-heapify the queue after removal
        self._rebalance_queue()  # Ensure the queue is ordered correctly

    def get_queue(self):
        # Return the current queue in descending order of age (oldest first)
        return [(name, age) for age, _, name in self.queue]

    def update_patient(self, old_name, new_name, new_age):
        # Update a patient's name and age
        for i, (age, _, name) in enumerate(self.queue):
            if name == old_name:
                # Update the patient's details in the queue
                self.queue[i] = (new_age, self.patient_count, new_name)
                self.patient_count += 1
                self._rebalance_queue()  # Ensure the queue is ordered correctly
                return True
        return False  # Return False if the patient wasn't found

# Testing the updated PriorityQueue class

# queue = PriorityQueue()

# Adding patients
# queue.add_patient("John Doe", 60)  # 60-year-old patient
# queue.add_patient("Jane Doe", 40)  # 40-year-old patient
# queue.add_patient("Alice Smith", 100)  # 100-year-old patient
# queue.add_patient("Bob Brown", 80)  # 80-year-old patient

# Print the queue sorted by age (oldest first)
# print(queue.get_queue())  # Expected output: [('Alice Smith', 100), ('Bob Brown', 80), ('John Doe', 60), ('Jane Doe', 40)]

# Call the first patient (oldest)
# print(queue.call_patient())  # Expected output: 'Alice Smith'

# Print the updated queue
# print(queue.get_queue())  # Expected output: [('Bob Brown', 80), ('John Doe', 60), ('Jane Doe', 40)]

