const csvParser = data => {
  const text = data.split(/\r\n|\n/)
  const [first, ...lines] = text
  const headers = first.split(';')
  const rows = []
  rows.headers = headers
  lines.map(line => {
    const values = line.split(';')
    const row = Object.fromEntries(headers.map((header, i) => [header, values[i]]))
    rows.push(row)
  })

  return rows
}

const markerIcon = color => L.divIcon({
  className: 'ship-div-icon',
  html: `<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" fill="${color}" ></svg>`
})

const map = L.map('map')

const locations = []

async function fillRiverStations () {
  const response = await fetch('/stations-river.txt')
  const text = await response.text()
  const stations = csvParser(text)

  for (const station of stations) {
    const location = [parseFloat(station.LAT), parseFloat(station.LON)]
    L.marker(location, { title: `River: ${station.NAME}, ${station.RIVER} (${station.CODE})`, icon: markerIcon('#00008b') }).addTo(map)
    locations.push(location)
  }
}

//await fillRiverStations()
//await fillRainStations()

locations.push([0,0])

map.fitBounds(L.latLngBounds(locations))

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map)
