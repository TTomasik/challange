import {useEffect, useState} from "react";
import './App.css';
import axios from 'axios';
import Characters from './Characters'
import Collections from './Collections'
import ValueCount from './ValueCount'
import {
    CHARACTERS_URL, COUNT_VALUES_URL, CSV_FILES_URL,
    FETCH_NEWEST_COLLECTION, LOAD_MORE_URL
} from './urls'


const SCOPE_COLLECTIONS = "collections";
const SCOPE_CHARACTERS = "characters";
const SCOPE_VALUE_COUNT = "valueCount";

const SCOPES = {
    [SCOPE_COLLECTIONS]: props => <Collections {...props}/>,
    [SCOPE_CHARACTERS]: props => <Characters {...props}/>,
    [SCOPE_VALUE_COUNT]: props => <ValueCount {...props}/>
}


const App = () => {
    const INIT_NMB_OF_CHARACTERS = 10;
    const [currentScope, setCurrentScope] = useState(SCOPE_COLLECTIONS);
    const [collections, setCollections] = useState([]);
    const [isFetching, setIsFetching] = useState(false);
    const [characters, setCharacters] = useState([]);
    const [csvId, setCsvId] = useState(null);
    const [nmbOfCharacters, setNmbOfCharacters] = useState(INIT_NMB_OF_CHARACTERS);
    const [valuesToCount, setValues] = useState([]);
    const [headers, setHeaders] = useState([]);

    useEffect(() => {
        axios.get(CSV_FILES_URL).then(response =>
            {setAllCollections(response.data)}
        );
    }, [isFetching]);

    const setAllCollections = collections => {
        setCollections(collections);
    }

    const onOpenCollection = csvId =>
        axios.get(CHARACTERS_URL(csvId)).then(response => {
            setCharacters(response.data.data);
            setCsvId(csvId);
            setCurrentScope(SCOPE_CHARACTERS);
            setHeaders(response.data.data[0])
        });

    const onFetchNewestCollection = () => {
        setIsFetching(isFetching => !isFetching);
        axios.post(FETCH_NEWEST_COLLECTION).then(response => {
            setIsFetching(isFetching => !isFetching);
        });
    }

    const onSetCurrentScope = () => {
        setCharacters([]);
        setCsvId(null);
        setCurrentScope(SCOPE_COLLECTIONS);
        setNmbOfCharacters(INIT_NMB_OF_CHARACTERS);
    }

    const onLoadMore = () => {
        const range = nmbOfCharacters + INIT_NMB_OF_CHARACTERS;
        axios.get(LOAD_MORE_URL(csvId, nmbOfCharacters, range)).then(response => {
            setCharacters([...characters, ...response.data.data.slice(1)]);
            setNmbOfCharacters(nmbOfCharacters + response.data.results);
        });
    }

    const onInitValueCount = () => {
        setCharacters([characters[0]]);
        setNmbOfCharacters(INIT_NMB_OF_CHARACTERS);
        setCurrentScope(SCOPE_VALUE_COUNT);
    }

    const onSetValues = newValue => {
        if (valuesToCount.includes(newValue)) {
            const newValues = valuesToCount.filter(value => value !== newValue);
            return setValues(newValues);
        }
        return setValues([...valuesToCount, newValue]);
    }

    const prepareURLValues = values => values.map(v => `&${v}=true`).join("");

    const onCountValues = () => {
        if (valuesToCount.length) {
            const values = prepareURLValues(valuesToCount);
            axios.get(COUNT_VALUES_URL(csvId, values)).then(response => {
                setCharacters(response.data.data);
            });
        }
    }

    const scopesProps = {
        [SCOPE_COLLECTIONS]: {
            collections: collections,
            isFetching: isFetching,
            onFetchNewestCollection: onFetchNewestCollection,
            onOpenCollection: onOpenCollection
        },
        [SCOPE_CHARACTERS]: {
            characters: characters,
            onInitValueCount: onInitValueCount,
            onLoadMore: onLoadMore
        },
        [SCOPE_VALUE_COUNT]: {
            characters: characters,
            headers: headers,
            onCountValues: onCountValues,
            onSetValues: onSetValues,
            valuesToCount: valuesToCount
        }
    }

    const backToCollectionsBtn = () => {
        if (currentScope !== SCOPE_COLLECTIONS) {
            return (
                <button
                    className="back-btn"
                    onClick={() => onSetCurrentScope()}
                >
                    ← BACK TO COLLECTIONS
                </button>
            );
        }
    };

    return (
        <div className="app">
            {backToCollectionsBtn()}
            {SCOPES[currentScope](scopesProps[currentScope])}
        </div>
    );
}

export default App;
