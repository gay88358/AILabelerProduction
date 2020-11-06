// data
const data = { x: 1, y: 2 }

// real data and deps behind
let realX = data.x
let realY = data.y
const realDepsX = []
const realDepsY = []

// make it reactive
Object.defineProperty(data, 'x', {
  get() {
    trackX()
    return realX
  },
  set(v) {
    realX = v
    triggerX()
  }
})
Object.defineProperty(data, 'y', {
  get() {
    trackY()
    return realY
  },
  set(v) {
    realY = v
    triggerY()
  }
})

// track and trigger a property
const trackX = () => {
  if (isDryRun && currentDep) {
    realDepsX.push(currentDep)
  }
}
const trackY = () => {
  if (isDryRun && currentDep) {
    realDepsY.push(currentDep)
  }
}
const triggerX = () => {
  realDepsX.forEach(dep => dep())
}
const triggerY = () => {
  realDepsY.forEach(dep => dep())
}

// observe a function
let isDryRun = false
let currentDep = null
const observe = fn => {
  isDryRun = true
  currentDep = fn
  fn()
  currentDep = null
  isDryRun = false
}

// define 3 functions
const depA = () => console.log(`x = ${data.x}`)
const depB = () => console.log(`y = ${data.y}`)
const depC = () => console.log(`x + y = ${data.x + data.y}`)

// dry-run all dependents
observe(depA)
observe(depB)
observe(depC)
// output: x = 1, y = 2, x + y = 3

// mutate data
data.x = 3
// output: x = 3, x + y = 5
data.y = 4
// output: y = 4, x + y = 7
