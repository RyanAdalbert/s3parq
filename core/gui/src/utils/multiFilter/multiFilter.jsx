/**
 * Filters an array of objects with multiple criteria.
 *
 * @param  {Array}  array: the array to filter
 * @param  {Object} filters: an object with the filter criteria as the property names
 * @return {Array}
 */

const multiFilter = (array, filters) => {
  const filterKeys = Object.keys(filters);
  // filters all elements passing the criteria
  return array.filter(item => {
    // dynamically validate all filter criteria
    return filterKeys.every(key => {
      // ignores an empty filter
      if (!filters[key].length) return true;
      console.log(item[key]);
      return filters[key].includes(item[key]);
    });
  });
};

export default multiFilter;
