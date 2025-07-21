import React from 'react';
import styles from '../../styles/ASLTranslator.styles';

const ErrorMessage = ({ error }) => {
  if (!error) return null;
  
  return (
    <div style={styles.error}>
      {error}
    </div>
  );
};

export default ErrorMessage; 