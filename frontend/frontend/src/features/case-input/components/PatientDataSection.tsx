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
    <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
      <h3 className="text-base font-medium text-gray-800 mb-4">
        Datos del paciente
      </h3>

      <div className="space-y-4">
        <div>
          <label htmlFor="patient-age" className="block text-sm text-gray-700 mb-1">
            Edad
          </label>
          <input
            id="patient-age"
            type="number"
            min={0}
            max={120}
            value={value.age}
            onChange={handleAgeChange}
            className="w-full max-w-[8rem] px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            aria-label="Edad"
          />
        </div>

        <fieldset>
          <legend className="block text-sm text-gray-700 mb-2">Sexo</legend>
          <div className="flex gap-4">
            <label className="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="patient-sex"
                value="Hombre"
                checked={value.sex === 'Hombre'}
                onChange={() => handleSexChange('Hombre')}
                className="text-emerald-600 focus:ring-emerald-500"
                aria-label="Hombre"
              />
              <span className="text-sm text-gray-800">Hombre</span>
            </label>
            <label className="inline-flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="patient-sex"
                value="Mujer"
                checked={value.sex === 'Mujer'}
                onChange={() => handleSexChange('Mujer')}
                className="text-emerald-600 focus:ring-emerald-500"
                aria-label="Mujer"
              />
              <span className="text-sm text-gray-800">Mujer</span>
            </label>
          </div>
        </fieldset>

        <div>
          <label className="inline-flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={value.isPregnant}
              onChange={handlePregnantChange}
              className="rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
              aria-label="Embarazo"
            />
            <span className="text-sm text-gray-800">Embarazo</span>
          </label>
        </div>
      </div>
    </div>
  )
}
