// api.js

export async function fetchTeams() {
  try {
    const response = await fetch('http://127.0.0.1:5003/teams');
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch teams:', response.statusText);
      return [];
    }
  } catch (error) {
    console.error('Error fetching teams:', error);
    return [];
  }
}