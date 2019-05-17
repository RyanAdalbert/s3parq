const mockPipelines = {
  1:{
    name: 'Whites Pipeline',
    brand: 'White Walkers',
    pharma_company: 'North o the Wall',
    type: 'Destruction',
    status: 'Complete',
    description: 'Army of the dead must be destroyed',
    run_freq: 'Once',
    states: ['Walking', 'Standing'],
    transformations: ['Lose Some', 'Raise More']
  },
  2:{
    name: 'Dragon Pipeline',
    brand: 'Huge Dragons',
    pharma_company: 'Targaryen',
    type: 'Attack Setup',
    status: 'In Progress',
    description: 'Dragons are on their way to kings Landing',
    run_freq: 'Once',
    states: ['Flying', 'Burning', 'Eating'],
    transformations: 'None'
  },
  3: {
    name: 'Wildlings Pipeline',
    brand: 'Mance Raiders',
    pharma_company: 'North o the Wall',
    type: 'Relocation',
    status: 'In Progress',
    description: 'The Wildlings are on the move to find a place to sleep.',
    run_freq: 'Weekly',
    states: ['Moving', 'Sleeping', 'Eating'],
    transformations: ['Make Friendly', 'Send Home']
  }
}