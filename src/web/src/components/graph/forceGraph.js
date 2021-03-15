import React from "react";
import { runForceGraph } from "./forceGraphGenerator";
import styles from "./Graph.module.css";

export function ForceGraph({ courseModal, coursesData, nodeHoverTooltip }) {
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    let destroyFn;

    if (containerRef.current) {
      const { destroy } = runForceGraph(courseModal, containerRef.current, coursesData, nodeHoverTooltip);
      destroyFn = destroy;
    }

    return destroyFn;
  });

  return <div ref={containerRef} className={styles.container} />;
}
