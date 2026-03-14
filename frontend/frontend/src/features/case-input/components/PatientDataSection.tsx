export interface PatientDataValue {
  age: string
  sex: 'Hombre' | 'Mujer' | null
  isPregnant: boolean
}

interface PatientDataSectionProps {
  value: PatientDataValue
  onChange: (value: PatientDataValue) => void
}

export function PatientDataSection({ value, onChange }: PatientDataSectionProps) {
  const handleAgeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({ ...value, age: e.target.value })
  }

  const handleSexChange = (sex: 'Hombre' | 'Mujer') => {
    onChange({ ...value, sex })
  }

  const handlePregnantChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({ ...value, isPregnant: e.target.checked })
  }

  return (
    <div className="bg-gray-50 rounded-lg p-6 mb-6">
      <h3 className="text-left text-gray-800 mb-4">
        Datos del paciente
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label htmlFor="patient-age" className="block text-gray-700 mb-2">
            Edad
          </label>
          <input
            id="patient-age"
            type="number"
            min={0}
            max={120}
            value={value.age}
            onChange={handleAgeChange}
            className="w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
            aria-label="Edad"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-3">Sexo</label>
        <fieldset>
          <legend className="sr-only">Sexo</legend>
          <div className="flex gap-4">
            <label className="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="patient-sex"
                value="Hombre"
                checked={value.sex === 'Hombre'}
                onChange={() => handleSexChange('Hombre')}
                className="w-4 h-4 text-emerald-500 focus:ring-emerald-500"
                aria-label="Hombre"
              />
              <span>Hombre</span>
            </label>
            <label className="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="patient-sex"
                value="Mujer"
                checked={value.sex === 'Mujer'}
                onChange={() => handleSexChange('Mujer')}
                className="w-4 h-4 text-emerald-500 focus:ring-emerald-500"
                aria-label="Mujer"
              />
              <span className="text-sm text-gray-800">Mujer</span>
            </label>
          </div>
        </fieldset>
        </div>

        <div>
          <label className="block text-gray-700 mb-3">Estado</label>
          <label className="inline-flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={value.isPregnant}
              onChange={handlePregnantChange}
              className="w-4 h-4 text-emerald-500 rounded focus:ring-emerald-500"
              aria-label="Embarazo"
            />
            <span>Embarazo</span>
          </label>
        </div>
      </div>
    </div>
  )
}
