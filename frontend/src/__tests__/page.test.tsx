import { render, screen } from '@testing-library/react'
import Home from '../app/page'

describe('Home', () => {
  it('renders the main heading', () => {
    render(<Home />)

    const heading = screen.getByRole('heading', {
      name: /ai analyst mvp/i,
    })

    expect(heading).toBeInTheDocument()
  })

  it('renders the description', () => {
    render(<Home />)

    const description = screen.getByText(/ai-powered analyst for startup pitch decks/i)

    expect(description).toBeInTheDocument()
  })
})