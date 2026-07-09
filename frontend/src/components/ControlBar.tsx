type Props = {
  currentIndex: number;
  maxIndex: number;
  onFirst: () => void;
  onPrev: () => void;
  onNext: () => void;
  onLast: () => void;
};

export default function ControlBar({
  currentIndex,
  maxIndex,
  onFirst,
  onPrev,
  onNext,
  onLast,
}: Props) {
  return (
    <div className="control-bar">
      <button onClick={onFirst} disabled={currentIndex <= -1}>{"<<"}</button>
      <button onClick={onPrev} disabled={currentIndex <= -1}>{"<"}</button>

      <span>
        {currentIndex < 0
          ? `Start position / ${maxIndex + 1} moves`
          : `Move ${currentIndex + 1} / ${maxIndex + 1}`}
      </span>

      <button onClick={onNext} disabled={currentIndex >= maxIndex}>{">"}</button>
      <button onClick={onLast} disabled={currentIndex >= maxIndex}>{">>"}</button>
    </div>
  );
}