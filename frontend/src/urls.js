export const CSV_FILES_URL = "http://127.0.0.1:8000/api/csv_files/";
export const CHARACTERS_URL = csvId => `http://127.0.0.1:8000/api/people?csv_id=${csvId}`;
export const FETCH_NEWEST_COLLECTION = "http://127.0.0.1:8000/api/fetch_newest_collection/";
export const LOAD_MORE_URL = (csvId, nmbOfCharacters, range) =>
    `http://127.0.0.1:8000/api/people?csv_id=${csvId}&start_idx=${nmbOfCharacters}&stop_idx=${range}`;
export const COUNT_VALUES_URL = (csvId, values) => `http://127.0.0.1:8000/api/value_count?csv_id=${csvId}${values}`;
