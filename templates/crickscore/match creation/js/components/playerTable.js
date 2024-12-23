export function createPlayerTable(players, onDelete) {
    const table = document.createElement('table');
    table.className = 'player-table';
    
    table.innerHTML = `
        <thead>
            <tr>
                <th>Player Name</th>
                <th>Age</th>
                <th>Role</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            ${players.map((player, index) => `
                <tr>
                    <td>${player.playerName}</td>
                    <td>${player.age}</td>
                    <td>${player.playerRole}</td>
                    <td>
                        <button class="delete-btn" data-index="${index}">Delete</button>
                    </td>
                </tr>
            `).join('')}
        </tbody>
    `;

    table.querySelectorAll('.delete-btn').forEach(btn => {
        btn.onclick = () => onDelete(parseInt(btn.dataset.index));
    });

    return table;
}