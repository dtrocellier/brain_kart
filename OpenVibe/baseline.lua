
function initialize(box)

	dofile(box:get_config("${Path_Data}") .. "/plugins/stimulation/lua-stimulator-stim-codes.lua")

	baseline_duration = box:get_setting(2)

end

function process(box)

	local t = 0

	-- manages baseline
	box:send_stimulation(1, OVTK_StimulationId_ExperimentStart, t, 0)
	t = t + baseline_duration
	
	box:send_stimulation(1, OVTK_StimulationId_ExperimentStop, t, 0)
	
end
