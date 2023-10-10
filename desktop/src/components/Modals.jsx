import React, {useEffect, useState} from 'react';
import {useChartData} from '@/context/chart';
import {useSettings} from '@/context/settings';
import {CloseIcon} from './SVGIcons';
import {BaseTextInput} from './Input';
import {editDataPoint} from '@/api';

/**
 * Edit a data point.
 *
 * @param {object} data - The data object.
 * @param {number} idx - The index of the data point.
 * @param {object} form - The form object.
 * @return {Promise} A promise that resolves with the updated data.
 */
export function ModalDataForm() {
  const {formModal, setFormModal} = useSettings();
  const [form, setForm] = useState({
    instruction: '',
    input: '',
    output: '',
  });
  const {data, setData} = useChartData();

  useEffect(() => {
    if (formModal && formModal.idx < data.length) {
      setForm({
        instruction: formModal.instruction,
        input: formModal.input,
        output: formModal.output,
      });
    }
  }, [formModal]);

  const handleFormChange = (e) => {
    const {name, value} = e.target;
    setForm((prevForm) => ({
      ...prevForm,
      [name]: value,
    }));
  };

  const closeModal = (e) => {
    if (e.target.id === 'dataFrom' || e.target.id === 'closeModal') {
      setFormModal(null);
    }
  };

  const editData = (e) => {
    e.stopPropagation();
    /** might want to refetch clustering */
    editDataPoint(data, formModal.idx, form).then((result) => {
      setData(result);
    });

    setFormModal(null);
  };

  return !formModal && formModal !== 0 ? (
    ''
  ) : (
    <div
      id="dataFrom"
      tabIndex="-1"
      aria-hidden="false"
      className="fixed top-0 left-0 right-0 z-50 w-screen
      p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-screen
      max-h-full flex justify-center items-center bg-slate-900/70"
      onClick={closeModal}
    >
      <div className="relative w-full max-w-2xl max-h-full">
        {/* Modal content */}
        <div className="relative bg-white rounded-lg shadow dark:bg-gray-700">
          {/* <!-- Modal header --> */}
          <div
            className="flex items-start justify-between
          p-4 border-b rounded-t dark:border-gray-600
          "
          >
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
              Edit Data
            </h3>
            <button className="p-1 bg-transparent">
              <CloseIcon id="closeModal" onClick={closeModal} />
            </button>
          </div>
          {/* <!-- Modal body --> */}
          <div className="p-6 space-y-2 text-left">
            <p
              className="text-base leading-relaxed
            text-gray-500 dark:text-gray-400 mb-4 text-center"
            >
              Some notes here.
            </p>
            <div>
              <label className="text-gray-400">Instruction</label>
              <BaseTextInput
                name="instruction"
                placeholder={`Edit Instruction`}
                className="bg-gray-200 text-gray-900 my-2"
                value={form.instruction}
                onChange={handleFormChange}
              />
            </div>
            <div>
              <label className="text-gray-400">Input</label>
              <BaseTextInput
                name="input"
                placeholder={`Edit Input`}
                className="bg-gray-200 text-gray-900 my-2"
                value={form.input}
                onChange={handleFormChange}
              />
            </div>
            <div>
              <label className="text-gray-400">Output</label>
              <BaseTextInput
                name="output"
                placeholder={`Edit Output`}
                className="bg-gray-200 text-gray-900 my-2"
                value={form.output}
                onChange={handleFormChange}
              />
            </div>
          </div>
          {/* <!-- Modal footer --> */}
          <div
            className="flex items-center p-6 space-x-2 border-t
           border-gray-200 rounded-b dark:border-gray-600"
          >
            <button
              data-modal-hide="defaultModal"
              type="button"
              onClick={editData}
              className="text-white bg-blue-700 hover:bg-blue-800
              focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium
              rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600
              dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              edit
            </button>
            <button
              id="closeModal"
              data-modal-hide="defaultModal"
              type="button"
              onClick={closeModal}
              className="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4
              focus:outline-none focus:ring-blue-300 rounded-lg border
              border-gray-200 text-sm font-medium px-5 py-2.5hover:text-gray-900
              focus:z-10 dark:bg-gray-700 dark:text-gray-300
              dark:border-gray-500 dark:hover:text-white
              dark:hover:bg-gray-600 dark:focus:ring-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Edit a data point.
 *
 * @param {object} data - The data object.
 * @param {number} idx - The index of the data point.
 * @param {object} form - The form object.
 * @return {Promise} A promise that resolves with the updated data.
 */
export function ModalTORPP() {
  const {formModal, setFormModal} = useSettings();

  const closeModal = (e) => {
    e.stopPropagation();
    if (e.target.id === 'dataFrom' || e.target.id === 'closeModal') {
      setFormModal(null);
    }
  };

  const editData = (e) => {
    e.stopPropagation();
    setFormModal(null);
  };

  return !formModal && formModal !== 0 ? (
    ''
  ) : (
    <div
      id="dataFrom"
      tabIndex="-1"
      aria-hidden="false"
      className="fixed top-0 left-0 right-0 z-50 w-screen p-4
      overflow-x-hidden overflow-y-auto md:inset-0 h-screen max-h-full
      flex justify-center items-center bg-slate-900/70"
      onClick={closeModal}
    >
      <div className="relative w-full max-w-2xl max-h-full">
        {/* Modal content */}
        <div className="relative bg-white rounded-lg shadow dark:bg-gray-700">
          {/* <!-- Modal header --> */}
          <div
            className="flex items-start justify-between p-4
          border-b rounded-t dark:border-gray-600"
          >
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
              Terms of Service
            </h3>
            <button
              type="button"
              className="text-gray-400 bg-transparent hover:bg-gray-200
              hover:text-gray-900 rounded-lg text-sm w-8 h-8 ml-auto inline-flex
              justify-center items-center dark:hover:bg-gray-600
              dark:hover:text-white"
              data-modal-hide="defaultModal"
            >
              <svg
                className="w-3 h-3"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 14 14"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                />
              </svg>
              <span className="sr-only">Close modal</span>
            </button>
          </div>
          {/* <!-- Modal body --> */}
          <div className="p-6 space-y-6">
            <p
              className="text-base leading-relaxed
            text-gray-500 dark:text-gray-400"
            >
              With less than a month to go before the European Union enacts new
              consumer privacy laws for its citizens, companies around the world
              are updating their terms of service agreements to comply.
            </p>
            <p
              className="text-base leading-relaxed
            text-gray-500 dark:text-gray-400"
            >
              The European Union’s General Data Protection Regulation (G.D.P.R.)
              goes into effect on May 25 and is meant to ensure a common set of
              data rights in the European Union. It requires organizations to
              notify users as soon as possible of high-risk data breaches that
              could personally affect them.
            </p>
          </div>
          {/* <!-- Modal footer --> */}
          <div
            className="flex items-center p-6 space-x-2 border-t
           border-gray-200 rounded-b dark:border-gray-600"
          >
            <button
              data-modal-hide="defaultModal"
              type="button"
              onClick={editData}
              className="text-white bg-blue-700 hover:bg-blue-800
              focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium
              rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600
              dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              edit
            </button>
            <button
              id="closeModal"
              data-modal-hide="defaultModal"
              type="button"
              onClick={closeModal}
              className="text-gray-500 bg-white hover:bg-gray-100
              focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg
              border border-gray-200 text-sm font-medium px-5 py-2.5
              hover:text-gray-900 focus:z-10 dark:bg-gray-700 dark:text-gray-300
              dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600
              dark:focus:ring-gray-600"
            >
              Decline
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
