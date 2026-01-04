import './ProfileResults.css';

const ProfileResults = ({ data, onReset }) => {
  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Profile Data</h2>
        <button onClick={onReset} className="btn btn-secondary btn-small">
          Scrape Another Profile
        </button>
      </div>

      <div className="results-content">
        <div className="result-card">
          <div className="result-icon">👤</div>
          <div className="result-info">
            <label>Name</label>
            <p>{data.name || 'N/A'}</p>
          </div>
        </div>

        <div className="result-card">
          <div className="result-icon">💼</div>
          <div className="result-info">
            <label>Position</label>
            <p>{data.position || 'N/A'}</p>
          </div>
        </div>

        <div className="result-card">
          <div className="result-icon">🏢</div>
          <div className="result-info">
            <label>Company</label>
            <p>{data.company || 'N/A'}</p>
          </div>
        </div>

        {(data.start_time || data.end_time) && (
          <div className="result-card">
            <div className="result-icon">📅</div>
            <div className="result-info">
              <label>Employment Period</label>
              <p>
                {data.start_time && <span>{data.start_time}</span>}
                {data.start_time && data.end_time && <span> - </span>}
                {data.end_time && <span>{data.end_time}</span>}
                {data.total_time && <span className="duration"> ({data.total_time})</span>}
              </p>
            </div>
          </div>
        )}

        {data.summary && (
          <div className="result-summary">
            <h3>Summary</h3>
            <p>{data.summary}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfileResults;

