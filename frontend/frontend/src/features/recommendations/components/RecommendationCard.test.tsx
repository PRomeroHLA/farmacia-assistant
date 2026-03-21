import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { RecommendationCard } from './RecommendationCard'
import type { ProductRecommendation } from '../../../shared/types'

describe('RecommendationCard', () => {
  const baseProduct: ProductRecommendation = {
    id: 'rec-1',
    name: 'Paracetamol 1g',
    category: 'Analgésico',
    reason: 'Indicado para dolor leve y fiebre.',
    badge: 'main',
  }

  it('renders product name', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(screen.getByText('Paracetamol 1g')).toBeInTheDocument()
  })

  it('renders category', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(screen.getByText('Analgésico')).toBeInTheDocument()
  })

  it('renders reason', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(
      screen.getByText('Indicado para dolor leve y fiebre.')
    ).toBeInTheDocument()
  })

  it('shows badge "Recomendación principal" when badge is main', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(
      screen.getByText('Recomendación principal')
    ).toBeInTheDocument()
  })

  it('shows badge "Alternativa" when badge is alternative', () => {
    const alt: ProductRecommendation = { ...baseProduct, badge: 'alternative' }
    render(<RecommendationCard product={alt} />)
    expect(screen.getByText('Alternativa')).toBeInTheDocument()
  })

  it('renders labeled price, margin, stock, units and format when provided', () => {
    const withMeta: ProductRecommendation = {
      ...baseProduct,
      price: '5.99€',
      commercialMargin: '1,30 €',
      stock: 'En stock',
      stockUnits: '24',
      format: '20 comprimidos',
    }
    render(<RecommendationCard product={withMeta} />)
    expect(screen.getByText('Precio')).toBeInTheDocument()
    expect(screen.getByText('5.99€')).toBeInTheDocument()
    expect(screen.getByText('Margen')).toBeInTheDocument()
    expect(screen.getByText('1,30 €')).toBeInTheDocument()
    expect(screen.getByText('Stock')).toBeInTheDocument()
    expect(screen.getByText('En stock')).toBeInTheDocument()
    expect(screen.getByText('Unidades')).toBeInTheDocument()
    expect(screen.getByText('24')).toBeInTheDocument()
    expect(screen.getByText('Formato')).toBeInTheDocument()
    expect(screen.getByText('20 comprimidos')).toBeInTheDocument()
  })

  it('does not render meta footer when price/stock/format/margin/units omitted', () => {
    render(<RecommendationCard product={baseProduct} />)
    expect(screen.queryByText('Precio')).not.toBeInTheDocument()
    expect(screen.queryByText('Stock')).not.toBeInTheDocument()
  })

  it('shows recommended-for block when recommendedFor is set', () => {
    const p: ProductRecommendation = {
      ...baseProduct,
      recommendedFor: 'Congestión nasal y rinorrea',
    }
    render(<RecommendationCard product={p} />)
    expect(screen.getByText('Recomendado para')).toBeInTheDocument()
    expect(
      screen.getByText('Congestión nasal y rinorrea')
    ).toBeInTheDocument()
  })

  it('applies distinct stock style for "En stock" vs "Pocas unidades"', () => {
    const enStock: ProductRecommendation = {
      ...baseProduct,
      stock: 'En stock',
    }
    const { unmount } = render(<RecommendationCard product={enStock} />)
    const enStockEl = screen.getByText('En stock')
    expect(enStockEl).toHaveClass('text-emerald-600')

    unmount()
    const pocas: ProductRecommendation = {
      ...baseProduct,
      stock: 'Pocas unidades',
    }
    render(<RecommendationCard product={pocas} />)
    const pocasEl = screen.getByText('Pocas unidades')
    expect(pocasEl).toHaveClass('text-amber-600')
  })

  it('calls onSelect with product when "Ver detalle" is clicked', async () => {
    const onSelect = vi.fn()
    render(<RecommendationCard product={baseProduct} onSelect={onSelect} />)
    const button = screen.getByRole('button', { name: /ver detalle/i })
    await userEvent.setup().click(button)
    expect(onSelect).toHaveBeenCalledWith(baseProduct)
  })
})
