import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { RecommendationCard } from './RecommendationCard'

describe('RecommendationCard', () => {
  const baseRecommendation = {
    id: 'rec-1',
    name: 'Paracetamol 1g',
    category: 'Analgésico',
    reason: 'Indicado para dolor leve y fiebre.',
    isMain: true,
  }

  it('muestra el nombre del producto', () => {
    render(<RecommendationCard recommendation={baseRecommendation} />)
    expect(screen.getByText('Paracetamol 1g')).toBeInTheDocument()
  })

  it('muestra la categoría farmacéutica', () => {
    render(<RecommendationCard recommendation={baseRecommendation} />)
    expect(screen.getByText('Analgésico')).toBeInTheDocument()
  })

  it('muestra el texto de la razón (reason)', () => {
    render(<RecommendationCard recommendation={baseRecommendation} />)
    expect(
      screen.getByText('Indicado para dolor leve y fiebre.')
    ).toBeInTheDocument()
  })

  it('muestra el badge "Recomendación principal" cuando isMain es true', () => {
    render(<RecommendationCard recommendation={baseRecommendation} />)
    expect(
      screen.getByText('Recomendación principal')
    ).toBeInTheDocument()
  })

  it('muestra el badge "Alternativa" cuando isMain es false', () => {
    const alt = { ...baseRecommendation, isMain: false }
    render(<RecommendationCard recommendation={alt} />)
    expect(screen.getByText('Alternativa')).toBeInTheDocument()
  })

  it('no muestra botón "Ver detalle" cuando no se pasa onSelect', () => {
    render(<RecommendationCard recommendation={baseRecommendation} />)
    expect(screen.queryByRole('button', { name: /ver detalle/i })).not.toBeInTheDocument()
  })

  it('muestra botón "Ver detalle" y llama onSelect con la recomendación al hacer clic', async () => {
    const onSelect = vi.fn()
    render(
      <RecommendationCard recommendation={baseRecommendation} onSelect={onSelect} />
    )
    const button = screen.getByRole('button', { name: /ver detalle/i })
    expect(button).toBeInTheDocument()

    const user = userEvent.setup()
    await user.click(button)
    expect(onSelect).toHaveBeenCalledTimes(1)
    expect(onSelect).toHaveBeenCalledWith(baseRecommendation)
  })
})
