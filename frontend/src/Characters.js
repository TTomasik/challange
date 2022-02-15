import PropTypes from "prop-types";


const Characters = ({characters, onLoadMore, onInitValueCount}) => {
    const headers = characters[0];
    const charactersData = characters.slice(1);
    return (
        <>
            <table>
                <tbody>
                <tr>
                    {headers.map((header, idx) => <th key={idx}>{header.toUpperCase()}</th>)}
                </tr>
                {
                    charactersData.map(
                        (character, idx) =>
                            <tr key={`1-${idx}`}>{character.map((value, idx) =>
                                <th key={`2-${idx}`}>{value}</th>)}</tr>
                    )
                }
                </tbody>
            </table>
            <button
                className="loadmore-btn"
                onClick={() => onLoadMore()}
            >
                LOAD MORE
            </button>
            <button
                className="loadmore-btn"
                onClick={() => onInitValueCount()}
            >
                VALUE COUNT
            </button>
        </>
    );
};

Characters.propTypes = {
    characters: PropTypes.array,
    onLoadMore: PropTypes.func,
    onInitValueCount: PropTypes.func
};

export default Characters;
