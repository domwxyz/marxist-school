const API_BASE_URL = 'http://localhost:8000/api';

export const fetchAllContent = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/content`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching content:', error);
    throw error;
  }
};
