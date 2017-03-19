import random


def use_all_data(training_data, tau):
    return training_data


stored_flat_training =[]
def use_random_subset_data(training_data, tau):
    global stored_flat_training
    if len(stored_flat_training) == 0:
        stored_flat_training = [item for sublist in training_data for item in sublist]
    sample_list = []
    while len(stored_flat_training) < tau:
        sample_list = sample_list + stored_flat_training
        tau -= len(stored_flat_training)
    sample_list = sample_list + random.sample(stored_flat_training, tau)
    return_list = [[] for _ in range(len(training_data))]

    for element in sample_list:
        return_list[element[1]].append(element)
    return return_list

def use_classed_subset_data(training_data, tau):
    per_class_count = tau / len(training_data)
    return_list = []
    for class_data in training_data:
        class_sample = []
        remaining = per_class_count
        while remaining > len(class_data):
            class_sample += class_data
            remaining -= len(class_data)
        return_list.append(class_sample + random.sample(class_data, remaining))
    return return_list


def report(classwide_correct_count, data_set):
    accuracy = 0.0
    detection_rate = 0.0
    total_tests = 0
    for i in range(len(classwide_correct_count)):
        total_tests += len(data_set[i])
        accuracy += classwide_correct_count[i][0]
        detection_rate += float(classwide_correct_count[i][0]) / len(data_set[i])

    return accuracy / total_tests, detection_rate / len(classwide_correct_count)
