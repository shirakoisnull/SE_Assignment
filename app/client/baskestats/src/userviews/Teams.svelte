<script>
  import { fetchTeams, viewTeam } from "../api.js";
  import { onMount } from "svelte";
  import BottomNavigation from "../BottomNavigation.svelte";
  import TeamModal from "../modals/TeamModal.svelte";
  import { SearchIcon, InfoIcon } from "svelte-feather-icons";
  let teams = [];
  let searchQuery = "";
  let showModal = false;
  let teamInfo = [];

  onMount(async () => {
    teams = await fetchTeams();
  });

  async function handleView(tId) {
    teamInfo = await viewTeam(tId);
    showModal = true;
  }

  $: visibleTeams = searchQuery
    ? teams.filter((team) => {
        return team[1].toLowerCase().includes(searchQuery.toLowerCase());
      })
    : teams;
</script>

{#if showModal}
  <TeamModal
    {showModal}
    results={teamInfo}
    closeModal={() => (showModal = false)}
  />
{/if}

<BottomNavigation />

<div class="page-section-title">
Teams
</div>

<div class="box">
<form name="search">
<!-- <SearchIcon/> -->
  <input
    class="search-box"
    type="text"
    bind:value={searchQuery}
    placeholder="Search team..."
  />
  </form>
</div>

<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Name</th>
      <!-- <th>City</th>
      <th>Wins</th>
      <th>Losses</th> -->
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {#each visibleTeams as team}
      <tr>
        <td>{team[1]}</td>
        <!-- <td>{team[2]}</td>
        <td>{team[3]}</td>
        <td>{team[4]}</td> -->
        <td>
          <button style="display:flex;align-items: center;"on:click={() => handleView(team[0])}><InfoIcon/></button>
        </td>
      </tr>
    {/each}
  </tbody>
</table>
</div>