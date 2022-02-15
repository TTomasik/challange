import PropTypes from "prop-types";


const Collections = ({collections, isFetching, onFetchNewestCollection, onOpenCollection}) => {
    return (
        <>
            {
                isFetching
                    ? <div className="fetching-info">Fetching the newest collection, please wait...</div>
                    : (
                        <button className="back-btn" onClick={() => onFetchNewestCollection()}>
                            FETCH NEW COLLECTION
                        </button>
                    )
            }
            {
                collections.map(coll =>
                    <div
                        className="link"
                        key={coll.id}
                        onClick={() => onOpenCollection(coll.id)}
                    >
                        {coll.filename}
                    </div>
                )
            }
        </>
    );
};

Collections.propTypes = {
    collections: PropTypes.array,
    isFetching: PropTypes.bool,
    onFetchNewestCollection: PropTypes.func,
    onOpenCollection: PropTypes.func
};

export default Collections;
