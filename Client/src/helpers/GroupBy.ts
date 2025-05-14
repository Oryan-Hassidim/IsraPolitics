const groupBy = <T, K extends keyof any>(arr: T[], key: (i: T) => K) => {
    const map = new Map<K, T[]>();
    arr.forEach((item) => {
        const groupKey = key(item);
        const collection = map.get(groupKey);
        if (!collection) {
            map.set(groupKey, [item]);
        } else {
            collection.push(item);
        }
    });
    return Array.from(map.entries()).map(([key, items]) => ({
        key,
        items,
    }));
};
export default groupBy;
