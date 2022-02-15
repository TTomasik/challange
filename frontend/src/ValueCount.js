import PropTypes from "prop-types";


const ValueCount = ({characters, headers, onCountValues, onSetValues, valuesToCount}) => {
    const charactersData = characters.length > 1 ? characters : [];
    return (
        <>
            {headers.map((header, idx) =>
                <div
                    className="link padded"
                    key={idx}
                    onClick={() => onSetValues(header)}
                >
                    {header.toUpperCase()}
                    {valuesToCount.includes(header) ? "✓" : ""}
                </div>
            )}
            <button
                className="valuescount-btn"
                onClick={() => onCountValues()}
            >
                COUNT VALUES
            </button>
            {
                charactersData.length
                    ? <table>
                        <tbody>
                        {charactersData.map((character, idx) =>
                            <tr key={`1-${idx}`}>{character.slice(0, character.length - 1).map((value, idx) =>
                                <th key={`2-${idx}`}>{value}</th>)}</tr>
                        )}
                        </tbody>
                    </table>
                    : null
            }
        </>
    );
};

ValueCount.propTypes = {
    characters: PropTypes.array,
    headers: PropTypes.array,
    onCountValues: PropTypes.func,
    onSetValues: PropTypes.func,
    valuesToCount: PropTypes.array
};

export default ValueCount;
