<script>
  export let showModal = false;
  export let results = [];
  export let closeModal = () => {};

</script>

{#if showModal}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div class="modal-overlay" on:click={closeModal}></div>
  <div class="modal">
    <!-- svelte-ignore a11y-no-static-element-interactions -->
      <button class="close-button" on:click={closeModal}>Close</button>
    <div class="modal-content">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="table-container">
      <table>
        <thead>
          <tr>
            <th> LOCATION </th>
            <th> DATE </th>
            <th> TIME </th>
            <th> TEAM 1 </th>
            <th> TEAM 2</th>
            <th> SCORE </th>
          </tr>
        </thead>
        <tbody>
          {#each results as result}
            <tr>
              <td>{result[1]}</td>
              <td>{result[2]}</td>
              <td>{result[3]}</td>
              {#if result[4]}
                {#each result[4].split(",") as value}
                  <td>{value}</td>
                {/each}
              {/if}
              {#if result[5]}
                <td>{result[5].replace(/,/g, "-")}</td>
              {/if}
            </tr>
            {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>
{/if}

<style>
  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(19, 19, 19, 0.901);
    padding: 20px;
    border: 1px solid #ff3e00;
    border-radius: 8px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
    z-index: 1000;
  }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
  }
</style>
