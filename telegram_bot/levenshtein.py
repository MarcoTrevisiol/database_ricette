def distance(left_str, right_str):
    memo = {}

    def distance_memoized(a_index, b_index):
        if a_index < 0:
            return b_index + 1
        if b_index < 0:
            return a_index + 1

        value = memo.get((a_index, b_index), None)
        if value is None:
            if left_str[a_index] == right_str[b_index]:
                value = distance_memoized(a_index - 1, b_index - 1)
            else:
                v1 = distance_memoized(a_index - 1, b_index - 1)
                v2 = distance_memoized(a_index, b_index - 1)
                v3 = distance_memoized(a_index - 1, b_index)
                value = 1 + min(v1, v2, v3)

            memo[(a_index, b_index)] = value

        return value

    return distance_memoized(a_index=len(left_str) - 1, b_index=len(right_str) - 1)
