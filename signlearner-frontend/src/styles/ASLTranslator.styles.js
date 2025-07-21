export const styles = {
  // Layout
  container: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    padding: "20px 0"
  },

  innerContainer: {
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "0 20px"
  },

  // Header
  header: {
    textAlign: "center",
    marginBottom: "40px",
    color: "white"
  },

  title: {
    fontSize: "3.5rem",
    fontWeight: "700",
    margin: "0",
    textShadow: "2px 2px 4px rgba(0,0,0,0.3)",
    letterSpacing: "2px",
    fontFamily: "'Lineto Circular Black', 'Arial Black', 'Helvetica Neue', sans-serif"
  },

  subtitle: {
    fontSize: "1.2rem",
    margin: "10px 0 0 0",
    opacity: "0.9",
    fontWeight: "300"
  },

  // Cards
  card: {
    background: "rgba(255, 255, 255, 0.95)",
    borderRadius: "20px",
    padding: "40px",
    marginBottom: "30px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
    backdropFilter: "blur(10px)"
  },

  smallCard: {
    background: "rgba(255, 255, 255, 0.95)",
    borderRadius: "16px",
    padding: "24px",
    marginBottom: "30px",
    boxShadow: "0 8px 25px rgba(0,0,0,0.1)"
  },

  // Search Form
  searchForm: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "20px"
  },

  input: {
    width: "100%",
    maxWidth: "600px",
    padding: "18px 24px",
    fontSize: "1.1rem",
    border: "2px solid #e0e0e0",
    borderRadius: "50px",
    outline: "none",
    transition: "all 0.3s ease",
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
  },

  inputFocus: {
    borderColor: "#667eea",
    boxShadow: "0 0 0 3px rgba(102, 126, 234, 0.1)"
  },

  buttonContainer: {
    display: "flex",
    gap: "15px",
    flexWrap: "wrap",
    justifyContent: "center"
  },

  // Buttons
  button: {
    padding: "16px 32px",
    fontSize: "1.1rem",
    fontWeight: "600",
    color: "white",
    border: "none",
    borderRadius: "50px",
    cursor: "pointer",
    transition: "all 0.3s ease",
    opacity: 1,
    transform: "scale(1)"
  },

  buttonDisabled: {
    cursor: "not-allowed",
    opacity: 0.7,
    transform: "scale(0.95)"
  },

  buttonPrimary: {
    background: "linear-gradient(45deg, #667eea, #764ba2)",
    boxShadow: "0 4px 15px rgba(102, 126, 234, 0.4)"
  },

  buttonSecondary: {
    background: "linear-gradient(45deg, #f093fb, #f5576c)",
    boxShadow: "0 4px 15px rgba(245, 87, 108, 0.4)"
  },

  buttonSuccess: {
    background: "linear-gradient(45deg, #10b981, #059669)",
    boxShadow: "0 4px 15px rgba(16, 185, 129, 0.4)"
  },

  buttonHover: {
    transform: "scale(1.05)"
  },

  // Messages
  error: {
    background: "rgba(239, 68, 68, 0.1)",
    border: "1px solid rgba(239, 68, 68, 0.3)",
    borderRadius: "12px",
    padding: "16px",
    margin: "20px 0",
    color: "#dc2626",
    fontSize: "1.1rem",
    textAlign: "center"
  },

  loading: {
    textAlign: "center",
    padding: "40px",
    color: "white",
    fontSize: "1.2rem"
  },

  // Loading Spinner
  spinner: {
    display: "inline-block",
    width: "40px",
    height: "40px",
    border: "4px solid rgba(255,255,255,0.3)",
    borderRadius: "50%",
    borderTopColor: "white",
    animation: "spin 1s linear infinite",
    marginBottom: "20px"
  },

  // Search Info
  searchInfo: {
    display: "flex",
    flexWrap: "wrap",
    alignItems: "center",
    gap: "20px",
    marginBottom: "20px"
  },

  badge: {
    color: "white",
    padding: "6px 12px",
    borderRadius: "20px",
    fontSize: "0.9rem",
    fontWeight: "600"
  },

  badgeSuccess: {
    backgroundColor: "#10b981"
  },

  badgeInfo: {
    backgroundColor: "#3b82f6"
  },

  // Enhancement Panel
  enhancementPanel: {
    background: "linear-gradient(135deg, #e0f2fe 0%, #f3e5f5 100%)",
    padding: "20px",
    borderRadius: "12px",
    border: "1px solid #bfdbfe"
  },

  enhancementHeader: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    marginBottom: "15px"
  },

  enhancementTitle: {
    fontSize: "1.1rem",
    fontWeight: "700",
    color: "#1e40af"
  },

  enhancementGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "20px"
  },

  enhancementSection: {
    fontSize: "0.9rem",
    fontWeight: "600",
    color: "#374151",
    marginBottom: "8px"
  },

  enhancementContent: {
    fontSize: "0.9rem",
    color: "#6b7280",
    backgroundColor: "rgba(255,255,255,0.7)",
    padding: "8px 12px",
    borderRadius: "8px"
  },

  // Video Grid
  videoGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
    gap: "25px"
  },

  // Video Card
  videoCard: {
    background: "white",
    borderRadius: "16px",
    padding: "20px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
    border: "1px solid #e5e7eb",
    transition: "transform 0.3s ease",
    cursor: "pointer"
  },

  videoCardHover: {
    transform: "translateY(-5px)"
  },

  videoHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: "15px"
  },

  videoTitle: {
    fontSize: "1.1rem",
    fontWeight: "700",
    color: "#1f2937",
    flex: "1"
  },

  videoDescription: {
    fontSize: "0.9rem",
    color: "#6b7280",
    marginBottom: "15px",
    fontWeight: "500"
  },

  videoWrapper: {
    position: "relative",
    paddingBottom: "56.25%",
    height: "0",
    overflow: "hidden",
    borderRadius: "12px",
    backgroundColor: "#f3f4f6"
  },

  videoIframe: {
    position: "absolute",
    top: "0",
    left: "0",
    width: "100%",
    height: "100%",
    border: "none",
    borderRadius: "12px"
  },

  videoFooter: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: "15px"
  },

  videoDuration: {
    fontSize: "0.85rem",
    color: "#9ca3af",
    fontWeight: "500"
  },

  videoLink: {
    color: "#3b82f6",
    textDecoration: "none",
    fontSize: "0.85rem",
    fontWeight: "600",
    padding: "6px 12px",
    borderRadius: "6px",
    backgroundColor: "rgba(59, 130, 246, 0.1)",
    transition: "all 0.3s ease"
  },

  videoLinkHover: {
    backgroundColor: "rgba(59, 130, 246, 0.2)"
  },

  // Section Headers
  sectionHeader: {
    color: "#374151",
    fontSize: "1.8rem",
    fontWeight: "700",
    marginBottom: "25px",
    textAlign: "center"
  },

  // Lesson specific
  lessonStep: {
    backgroundColor: "#f093fb",
    color: "white",
    padding: "8px 12px",
    borderRadius: "20px",
    fontSize: "0.9rem",
    fontWeight: "600"
  },

  lessonLink: {
    color: "#f093fb",
    textDecoration: "none",
    fontSize: "0.85rem",
    fontWeight: "600",
    padding: "6px 12px",
    borderRadius: "6px",
    backgroundColor: "rgba(240, 147, 251, 0.1)",
    transition: "all 0.3s ease"
  },

  lessonLinkHover: {
    backgroundColor: "rgba(240, 147, 251, 0.2)"
  },

  // Variations
  variationList: {
    maxHeight: "120px",
    overflowY: "auto",
    fontSize: "0.85rem"
  },

  variationItem: {
    padding: "6px 12px",
    margin: "4px 0",
    borderRadius: "6px",
    backgroundColor: "rgba(255,255,255,0.7)",
    color: "#6b7280",
    fontWeight: "400",
    border: "1px solid transparent"
  },

  variationItemBest: {
    backgroundColor: "rgba(16, 185, 129, 0.1)",
    color: "#059669",
    fontWeight: "600",
    border: "1px solid #10b981"
  },

  // Confidence
  confidenceBox: {
    marginTop: "15px",
    padding: "10px 15px",
    backgroundColor: "rgba(59, 130, 246, 0.1)",
    borderRadius: "8px",
    fontSize: "0.9rem",
    color: "#1e40af"
  },

  // Lesson Options
  lessonOptions: {
    marginTop: "20px",
    padding: "20px",
    backgroundColor: "rgba(240, 147, 251, 0.05)",
    borderRadius: "12px",
    border: "1px solid rgba(240, 147, 251, 0.2)"
  },

  lessonOptionsTitle: {
    fontSize: "1.2rem",
    fontWeight: "700",
    color: "#7c3aed",
    marginBottom: "20px",
    textAlign: "center"
  },

  optionGroup: {
    marginBottom: "20px"
  },

  label: {
    display: "block",
    fontSize: "1rem",
    fontWeight: "600",
    color: "#374151",
    marginBottom: "8px"
  },

  radioGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "10px"
  },

  radioLabel: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "0.95rem",
    color: "#4b5563",
    cursor: "pointer",
    padding: "8px 12px",
    borderRadius: "8px",
    backgroundColor: "rgba(255, 255, 255, 0.7)",
    transition: "all 0.2s ease"
  },

  radioLabelHover: {
    backgroundColor: "rgba(240, 147, 251, 0.1)"
  },

  select: {
    width: "100%",
    padding: "12px 16px",
    fontSize: "1rem",
    border: "2px solid #e5e7eb",
    borderRadius: "8px",
    backgroundColor: "white",
    outline: "none",
    transition: "all 0.3s ease"
  },

  selectFocus: {
    borderColor: "#f093fb",
    boxShadow: "0 0 0 3px rgba(240, 147, 251, 0.1)"
  },

  // Performance Badge
  performanceBadge: {
    backgroundColor: "rgba(16, 185, 129, 0.1)",
    color: "#059669",
    padding: "6px 12px",
    borderRadius: "20px",
    fontSize: "0.9rem",
    fontWeight: "600",
    border: "1px solid rgba(16, 185, 129, 0.3)"
  },

  // Lesson Plan Display
  lessonHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
    flexWrap: "wrap",
    gap: "15px"
  },

  lessonTitle: {
    fontSize: "2rem",
    fontWeight: "700",
    color: "#1f2937",
    margin: "0"
  },

  lessonGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
    gap: "25px"
  },

  lessonSection: {
    backgroundColor: "rgba(255, 255, 255, 0.7)",
    padding: "20px",
    borderRadius: "12px",
    border: "1px solid #e5e7eb"
  },

  sectionTitle: {
    fontSize: "1.3rem",
    fontWeight: "700",
    color: "#374151",
    marginBottom: "15px",
    display: "flex",
    alignItems: "center",
    gap: "8px"
  },

  lessonInfo: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
    gap: "15px"
  },

  infoItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 15px",
    backgroundColor: "rgba(255, 255, 255, 0.8)",
    borderRadius: "8px",
    border: "1px solid #e5e7eb"
  },

  infoLabel: {
    fontSize: "0.9rem",
    fontWeight: "600",
    color: "#6b7280"
  },

  infoValue: {
    fontSize: "0.9rem",
    fontWeight: "700",
    color: "#374151"
  },

  vocabularyGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))",
    gap: "10px",
    marginBottom: "15px"
  },

  vocabularyItem: {
    backgroundColor: "rgba(240, 147, 251, 0.1)",
    color: "#7c3aed",
    padding: "8px 12px",
    borderRadius: "20px",
    fontSize: "0.9rem",
    fontWeight: "600",
    textAlign: "center",
    border: "1px solid rgba(240, 147, 251, 0.3)"
  },

  vocabularyStats: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap"
  },

  statBadge: {
    backgroundColor: "rgba(59, 130, 246, 0.1)",
    color: "#1e40af",
    padding: "6px 12px",
    borderRadius: "15px",
    fontSize: "0.85rem",
    fontWeight: "600"
  },

  objectiveList: {
    listStyle: "none",
    padding: "0",
    margin: "0"
  },

  objectiveItem: {
    padding: "8px 0",
    borderBottom: "1px solid #e5e7eb",
    fontSize: "0.95rem",
    color: "#374151",
    display: "flex",
    alignItems: "flex-start",
    gap: "8px"
  },

  objectiveItemBefore: {
    content: '""',
    fontSize: "1rem"
  },

  grammarList: {
    listStyle: "none",
    padding: "0",
    margin: "0"
  },

  grammarItem: {
    padding: "8px 0",
    borderBottom: "1px solid #e5e7eb",
    fontSize: "0.95rem",
    color: "#374151",
    display: "flex",
    alignItems: "flex-start",
    gap: "8px"
  },

  grammarItemBefore: {
    content: '""',
    fontSize: "1rem"
  },

  activityList: {
    listStyle: "none",
    padding: "0",
    margin: "0"
  },

  activityItem: {
    padding: "8px 0",
    borderBottom: "1px solid #e5e7eb",
    fontSize: "0.95rem",
    color: "#374151",
    display: "flex",
    alignItems: "flex-start",
    gap: "8px"
  },

  activityItemBefore: {
    content: '""',
    fontSize: "1rem"
  },

  culturalNotes: {
    backgroundColor: "rgba(245, 158, 11, 0.1)",
    color: "#92400e",
    padding: "15px",
    borderRadius: "8px",
    fontSize: "0.95rem",
    lineHeight: "1.5",
    border: "1px solid rgba(245, 158, 11, 0.3)"
  },

  similarityScore: {
    backgroundColor: "rgba(16, 185, 129, 0.1)",
    color: "#059669",
    padding: "4px 8px",
    borderRadius: "12px",
    fontSize: "0.8rem",
    fontWeight: "600"
  },

  noVideo: {
    backgroundColor: "#f3f4f6",
    border: "2px dashed #d1d5db",
    borderRadius: "12px",
    padding: "40px 20px",
    textAlign: "center"
  },

  noVideoText: {
    color: "#6b7280",
    fontSize: "1rem",
    fontWeight: "500"
  },

  lessonFooter: {
    marginTop: "30px",
    paddingTop: "20px",
    borderTop: "1px solid #e5e7eb"
  },

  lessonMeta: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "15px"
  },

  metaItem: {
    fontSize: "0.9rem",
    color: "#6b7280",
    fontWeight: "500"
  },

  // Performance Metrics
  metricsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "20px"
  },

  metricItem: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    padding: "15px",
    backgroundColor: "rgba(255, 255, 255, 0.8)",
    borderRadius: "12px",
    border: "1px solid #e5e7eb"
  },

  metricIcon: {
    fontSize: "2rem",
    width: "50px",
    textAlign: "center"
  },

  metricContent: {
    flex: "1"
  },

  metricLabel: {
    fontSize: "0.85rem",
    fontWeight: "600",
    color: "#6b7280",
    marginBottom: "4px"
  },

  metricValue: {
    fontSize: "1.2rem",
    fontWeight: "700",
    color: "#1f2937",
    marginBottom: "2px"
  },

  metricSpeed: {
    fontSize: "0.8rem",
    color: "#9ca3af",
    fontWeight: "500"
  }
};

export default styles; 