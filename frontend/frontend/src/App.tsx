import { RecommendationCard } from './features/recommendations/components/RecommendationCard.tsx'

function App() {
  const recommendation = {
    id: 'test-1',
    name: 'Spray bucofaríngeo X',
    category: 'Antisépticos',
    reason: 'Indicado para irritación faríngea leve',
    isMain: true,
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8">
      <div className="mx-auto max-w-xl">
        <RecommendationCard
          recommendation={recommendation}
          onSelect={(rec) => {
            // eslint-disable-next-line no-console
            console.log('Seleccionada recomendación de prueba', rec)
          }}
        />
      </div>
    </main>
  )
}

export default App
