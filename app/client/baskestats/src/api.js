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

export async function fetchPlayers() {
  try {
    const response = await fetch('http://127.0.0.1:5002/players');
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch players:', response.statusText);
      return [];
    }
  } catch (error) {
    console.error('Error fetching players:', error);
    return [];
  }
}

export async function fetchChampionships() {
  try {
    const response = await fetch('http://127.0.0.1:5004/championships');
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch championships:', response.statusText);
      return [];
    }
  } catch (error) {
    console.error('Error fetching championships:', error);
    return [];
  }
}
export async function fetchMatches(cId) {
  try {
    const response = await fetch(`http://127.0.0.1:5005/championships/${cId}/matches`);
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch matches:', response.statusText);
      return [];
    }
  } catch (error) {
    console.error('Error fetching matches:', error);
    return [];
  }
}

export async function viewTeam(tId) {
  try {
    const response = await fetch(`http://127.0.0.1:5003/teams/${tId}`);
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch team:', response.statusText);
      return [];
    }
  } catch (error) {
    console.error('Error fetching team:', error);
    return [];
  }
}