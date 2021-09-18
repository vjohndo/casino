// This script checks hidden checkboxes when a card is selected
const selectedCard = (event) => {
    event.target.classList.toggle('selected')
    const cardID = event.target.id
    const checkboxID = '#checkbox'+cardID[3]
    const checkbox = document.querySelector(checkboxID)
    checkbox.checked = !checkbox.checked
    console.log('This was clicked')
}

const pokerCards = document.querySelectorAll('.playingCard')

for (let card of pokerCards) {
    card.addEventListener('click', selectedCard)
}
