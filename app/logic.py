# Define position rules
RULE = {
    'application': 'openoffice',
    'coordinates': {
        'top-left': {'lat': 60.187372, 'lon': 24.820325},
        'bottom-right': {'lat': 60.186569, 'lon': 24.822551}
    }
}


def order_by_location(vm_instances, location):
    # Get rules
    coordinates = RULE['coordinates']
    application = RULE['application']

    # Define random ordered instances dict
    random_ordered_instances = {k: v for k, v in enumerate(vm_instances)}

    is_within = is_within_location(
        location,
        coordinates['top-left']['lat'],
        coordinates['top-left']['lon'],
        coordinates['bottom-right']['lat'],
        coordinates['bottom-right']['lon']
    )

    # If not within: check that it's not first
    if not is_within:
        # If not first: return instances how they are
        if random_ordered_instances[0]['name'] != application:
            return random_ordered_instances

        # Otherwise swap with last
        last_index = len(vm_instances) - 1

        temp = random_ordered_instances[0]
        random_ordered_instances[0] = random_ordered_instances[last_index]
        random_ordered_instances[last_index] = temp

        return random_ordered_instances

    else:
        # If first: return instances how they are
        if random_ordered_instances[0]['name'] == application:
            return random_ordered_instances

        # Otherwise put in first position
        current_index = None
        for index, instance in random_ordered_instances.iteritems():
            if instance['name'] == application:
                current_index = index

        temp = random_ordered_instances[0]
        random_ordered_instances[0] = random_ordered_instances[current_index]
        random_ordered_instances[current_index] = temp

        return random_ordered_instances


def is_within_location(location, lat1, lon1, lat2, lon2):
    """
    Return true if location is within given coordinates
    :param location:
    :param lat1:
    :param lon1:
    :param lat2:
    :param lon2:
    :return:
    """

    if lat1 >= float(location['latitude']) >= lat2 and lon1 <= float(location['longitude']) <= lon2:
        return True
    else:
        return False
