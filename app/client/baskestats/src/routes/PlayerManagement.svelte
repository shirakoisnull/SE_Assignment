<script>
 // import ConfirmationModal from "../ConfirmationModal.svelte";
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing";

  // Initialize teams as an empty array
  let players = [];

  // Fetch teams data from the backend
  async function fetchPlayers() {
    try {
      const response = await fetch("http://127.0.0.1:5002/players"); // Replace with your API endpoint
      if (response.ok) {
        const playerData = await response.json();

        // Assuming the structure is [[team_id, team_name, team_city, team_wins, team_losses], ...]
        players = playerData.map((player) => ({
          pid: player[0],
          tid: player[1],
          name: player[2],
          age: player[3],
          height: player[4],
          weight: player[5],
          pointsScored: player[6],
          // playsOn: player[7],
        }));

        // teams array assumed to be an array of objects with specific properties for each team
      } else {
        console.error("Failed to fetch players:", response.status);
        // Handle error
      }
    } catch (error) {
      console.error("Error fetching players:", error);
      // Handle error
    }
  }

  // Fetch player data on component mount
  onMount(fetchPlayers);

  function handleClick(event) {
    navigate("/newplayer");
  }

  async function deletePlayer(player) {
    const confirmation = window.confirm(`Are you sure you want to delete ${player.name}?`);
    if (confirmation) {
      try {
        const response = await fetch(`http://127.0.0.1:5002/players/${player.pid}`, {
          method: "DELETE",
        });

        if (response.ok) {
          fetchPlayers();
          console.log("Player deleted successfully!");
          alert(`Deleted ${player.name}`);
          // Perform any necessary actions upon successful deletion
          // For example, update the UI or reload team list
        } else {
          console.error("Failed to delete player:", response.statusText);
        }
      } catch (error) {
        console.error("Error deleting player:", error);
      }
      console.log("Deleted!");
    }
  }

  function handleUpdate(player) {
    navigate(`/editplayer`, { state: { player } });
  }

  let searchQuery = "";
  $: visiblePlayers = searchQuery ?
    players.filter(player=> {
      return (
        player.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }) : players;

</script>

<h1>Player Management</h1>

<!-- Search Box -->
<div class="box">
  <input
    class="search-box"
    type="text"
    bind:value={searchQuery}
    placeholder="Search player..."
  />
  </div>

  <button on:click={handleClick}>Create New Player</button>

<table>
  <thead>
    <tr>
      <th>PlayerID</th>
      <th>TeamID</th>
      <th>Name</th>
      <th>Age</th>
      <th>Height</th>
      <th>Weight</th>
      <th>Points</th>
      <!-- <th>Plays on</th> -->
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {#each visiblePlayers as player}
      <tr>
        <td>{player.pid}</td>
        <td>{player.tid}</td>
        <td>{player.name}</td>
        <td>{player.age}</td>
        <td>{player.height}</td>
        <td>{player.weight}</td>
        <td>{player.pointsScored}</td>
        <!-- <td>{player.playsOn}</td> -->
        <td>
          <button on:click={() => handleUpdate(player)}>Update</button>
          <button class="delete-button" on:click={() => deletePlayer(player)}>Delete</button>
        </td>
      </tr>
    {/each}
  </tbody>
</table>

<button class="back-button" on:click={() => navigate("/secretary")}>Go Back</button>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin: auto; /* Center the table horizontally */
  }

  th,
  td {
    padding: 10px;
    border: 1px solid #ccc;
    text-align: left;
  }

  th {
    /* background-color: #f2f2f2; */
    font-weight: bold;
  }

  tr:hover {
    background-color: #e9e9e921;
  }

  /* Style for update and delete buttons */
  button {
    padding: 6px 10px;
    margin: 2px;
    cursor: pointer;
    color: white;
    /* border: none; */
    border-radius: 4px;
  }

   /* Style the back button */
   .back-button {
    position: absolute;
    top: 20px;
    left: 20px;
    padding: 10px;
    background-color: #ff4000;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

</style>
