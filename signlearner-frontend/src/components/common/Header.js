import React from 'react';
import styles from '../../styles/ASLTranslator.styles';

const Header = ({ title, subtitle }) => {
  return (
    <div style={styles.header}>
      <h1 style={styles.title}>{title}</h1>
      <p style={styles.subtitle}>{subtitle}</p>
    </div>
  );
};

export default Header; 