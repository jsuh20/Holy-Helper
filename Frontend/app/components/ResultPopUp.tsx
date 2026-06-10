import '../style_css/ResultPopUp.css';


interface ResultPopUpProps {
    data: any;
    onClose: () => void;
  }

export default function ResultPopUp({ data, onClose }: ResultPopUpProps) {

    return (
        <>
            <div className="popup-overlay" onClick={onClose} />
            <div className="popup-container">
                <button className="popup-close" onClick={onClose}>
                ×
                </button>
                <h3 className="popup-title">Emotion Analysis Result</h3>
                <div className="popup-content">
                    <p>Because you are {data.emotion.toLowerCase()}</p>
                    <p>Verse: {data.bible_verse}</p>
                </div>
            </div>
        </>
    );
}