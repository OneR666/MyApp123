import random
import itertools
from typing import List, Tuple, Dict, Set

class CombinationGenerator:
    def generate_random_samples(self, m: int, n: int) -> List[int]:
        """Generate n unique random samples from 1..m, sorted."""
        nums = list(range(1, m + 1))
        selected = random.sample(nums, n)
        return sorted(selected)

    def generate_combinations(self, samples: List[int], k: int, j: int, s: int) -> List[List[int]]:
        """
        Generate a minimal set of k-combinations that covers all j-subsets of samples,
        where coverage means each j-subset has at least s elements in common with
        at least one chosen k-combination.
        """
        # 所有 k-组合 和 j-子集
        combos: List[Tuple[int, ...]] = list(itertools.combinations(samples, k))
        j_subsets: List[Tuple[int, ...]] = list(itertools.combinations(samples, j))

        # 构建映射：j_subset -> [combo_indices]
        j_to_combos: Dict[Tuple[int, ...], List[int]] = {js: [] for js in j_subsets}
        # 构建映射：combo_index -> set(j_subsets)
        combos_to_js: Dict[int, Set[Tuple[int, ...]]] = {i: set() for i in range(len(combos))}

        # 填充映射
        for idx, combo in enumerate(combos):
            combo_set = set(combo)
            for js in j_subsets:
                if len(combo_set.intersection(js)) >= s:
                    j_to_combos[js].append(idx)
                    combos_to_js[idx].add(js)

        # 初始未覆盖的 j-子集集合
        uncovered: Set[Tuple[int, ...]] = set(j_subsets)
        # 每个 combo 当前还能覆盖多少未覆盖 j-子集
        cover_counts: Dict[int, int] = {
            idx: len(combos_to_js[idx]) for idx in range(len(combos))
        }

        result: List[List[int]] = []

        # 贪心迭代
        while uncovered:
            # 找到覆盖最多未覆盖 j-子集的 combo
            best_idx, best_count = max(cover_counts.items(), key=lambda x: x[1])
            if best_count == 0:
                # 无法再覆盖任何新的 j-子集
                break

            # 记录最佳组合
            best_combo = combos[best_idx]
            result.append(list(best_combo))

            # 对该 combo 实际覆盖到的 j-子集进行移除，并更新其它 combo 的计数
            to_remove = combos_to_js[best_idx] & uncovered
            for js in to_remove:
                # 对每一个被移除的 j-子集，找到所有能覆盖它的 combo 并计数减一
                for idx2 in j_to_combos[js]:
                    cover_counts[idx2] -= 1
                uncovered.remove(js)

            # 该 combo 的计数置零，避免重复选择
            cover_counts[best_idx] = 0

        return result
