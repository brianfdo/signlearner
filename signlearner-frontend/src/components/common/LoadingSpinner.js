import React from 'react';
import styles from '../../styles/ASLTranslator.styles';

const LoadingSpinner = ({ message = "Searching for ASL videos..." }) => {
  return (
    <div style={styles.loading}>
      <div style={styles.spinner}></div>
      <div>{message}</div>
    </div>
  );
};

export default LoadingSpinner; 