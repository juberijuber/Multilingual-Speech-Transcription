/**
 * WaveformVisualizer.jsx — Animated audio level bars shown during recording.
 */

import { useMemo } from 'react';

const BAR_COUNT = 16;

export default function WaveformVisualizer({ audioLevel, isActive }) {
  // Generate bar heights based on audio level with some randomness
  const bars = useMemo(() => {
    return Array.from({ length: BAR_COUNT }, (_, i) => {
      const center = BAR_COUNT / 2;
      const distFromCenter = Math.abs(i - center) / center;
      const baseHeight = isActive ? (audioLevel / 100) * (1 - distFromCenter * 0.5) : 0.05;
      const jitter = isActive ? Math.random() * 0.3 : 0;
      return Math.max(0.05, Math.min(1, baseHeight + jitter));
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [audioLevel, isActive]);

  return (
    <div className="waveform" role="img" aria-label={isActive ? 'Recording audio level visualizer' : 'Audio visualizer inactive'}>
      {bars.map((h, i) => (
        <div
          key={i}
          className={`waveform-bar ${isActive ? 'recording' : ''}`}
          style={{ height: `${h * 36}px` }}
        />
      ))}
    </div>
  );
}
