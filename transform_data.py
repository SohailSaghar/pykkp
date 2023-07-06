from pymongo import MongoClient
import base64


# Notes:
# https://harddrop.com/forums/index.php?showtopic=7087&st=135
# very well explained above. reads 16 bits where the first 12 bits are timestamp of the movement and last 4 bits of
# 16 bits are what move was made. so we need to flip the below to number (key) to movement (value)
# https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)To_Binary('Space',8)&input=QjRjTzV4RlFGZUlaVnhweEhLb2ZReUVBSStjbGNpZ0ZMa2N3Z1RIME9PRTY1ejRoUXJORnNFWFVSM2RNQUUwa1VFSldOMXF3WFlkZnNXUVRaMlJwQjJvUmJuTndzSFNYZHJGM3BYclhmVUNDUW9WWGg4U050NDNSajlXUzQ1WVhtYVNhb0o2SG9yR201NmxBcW5TdUFySlh0ZlM3MTc5QXYxVEQ0c1pSeW9mT3RkTFgxVURWWk5teTNGZmRjZUlUNVNUbHgrY1E2M0x0RWZKWDlJSDcwZjNIQVhBRVJ3ZUJDOU1PQUErM0VmRVdReG1VRzFjZHNDTFNKYmNuNVNmaEwwRXhWelRrTnBFNXR6MGdRZ0pFSjBmRVNLQk1oMDJoVDZWU28xY1hXVUZkVjErQlpHTmw4R2ZIYWtSdElXK1VjVWR6Y1hnamVmQjd0MzAwZm5LREY0UWhoeldJMDQySGtCU1NBSmIzbUZDWmhKeWlvTlNpaDZuSHJFQ3hrclZYdTVlLzhjUXp4M0RLUjh5QnpvWFFzOU8zMWZIYkk5MmszamZpY2VlMzZNSHQ0L0FGOEFQek4vYWcrM0w5d1FEbkF5RUlFd3EwREdjUGxSUEhGU0Fad2gwM0hmSWhnU2FuS0FBc2dqSTNPWGM4c1QyMVJCRkhGMGlBVE5KUGtWUzNXZmRjSVdDVFkyVm1sMmtBYVJSdUluQjBjaGQwTVhWRmU2RjlsNEVraERDSEo0aEJqV09RNUpHWGxMV1VzWm9IbkFHZEZhRXpvMmVqb0toeXJkZXQ0YkxqdEhDMWxMaFh1OEMrQk1HM3hOWEpCOHVBMEFMVGw5ZkIydGZkQWVIRDVkVG5oK3dVN2hEMGRQZzMrbEg4ZGY3akF0Y0VJQWh5RERjT3NCS0hFN0VZRXhvZ0hvUWdKeUpoSnBNckZDM1hNUUUxTXppME9VYytoVDZoUWVkRThVWGxTZ05MRjA2Z1UySld0MW9nWHZKbVoyd1VjdmQ1UlhsaGdLR0R4NFkwaURDTUo0NXdrdktXaDVhaG0xT2RWSjFUb1Fla01hV2txbmVzbGF5eHNkZTBVTG1DdldmQjRNVzN5ZkhLNWM1VDAyWFRzTlZuMk1MZDErQUI0UFhrTStjMzZYSHVvKzd3OGJmek5QUFMrcFQ3SndPM0J2b0g4UXIxRE9NUlJ4U3FHTUViTkNBUkpDYz0
# decodes from base64 to binary.


def base64_to_binary(base64_string):
    data_in_bytes = base64.b64decode(base64_string)
    binary_string = ''.join(format(byte, '08b') for byte in data_in_bytes)
    binary_string_with_spaces = ' '.join(binary_string[i:i + 16] for i in range(0, len(binary_string), 16))
    list_of_moves_in_binary = binary_string_with_spaces.split(" ")
    # remove last element, because this is not a part of the game.
    list_of_moves_in_binary.pop()
    return list_of_moves_in_binary


def transform_data(game_data, collection):
    # transformation is explained well in this blog post:
    # https://harddrop.com/forums/index.php?showtopic=7087&st=135
    gameplay_in_base64 = game_data["d"]
    gameplay_in_binary = base64_to_binary(gameplay_in_base64)
    movement = {0: 'MOVE_LEFT', 1: 'MOVE_RIGHT', 2: 'DAS_LEFT', 3: 'DAS_RIGHT',
                4: 'ROTATE_LEFT', 5: 'ROTATE_RIGHT', 6: 'ROTATE_180', 7: 'HARD_DROP',
                8: 'SOFT_DROP_BEGIN_END', 9: 'GRAVITY_STEP', 10: 'HOLD_BLOCK', 11: 'GARBAGE_ADD',
                12: 'SGARBAGE_ADD', 13: 'REDBAR_SET', 14: 'ARR_MOVE', 15: 'AUX'}
    list_of_moves = []
    move_number = 0
    iteration = 0
    current_timestamp = -1
    for move in gameplay_in_binary:
        time_and_command = {}
        timestamp = int(move[0:12], 2) * 0.001
        command = movement[int(move[12:16], 2)]
        if current_timestamp <= timestamp:
            current_timestamp = timestamp
        else:
            iteration += 1
            current_timestamp = -1
        time_and_command["move_number"] = move_number
        time_and_command["timestamp_in_seconds"] = round(timestamp + 4.094 * iteration, ndigits=3)
        time_and_command["command"] = command
        list_of_moves.append(time_and_command)
        move_number += 1
    collection.insert_one({"gameplay": list_of_moves, "d": game_data})
    print("game movements for the game id:", game_data["id"])


def main():
    client = MongoClient("localhost", 27017)
    db = client["jstris"]
    collection_data = db["games"]
    collection_to_save = db["game_movements"]
    entries = list(collection_data.find())
    for entry in entries:
        transform_data(entry, collection_to_save)


if __name__ == '__main__':
    main()
