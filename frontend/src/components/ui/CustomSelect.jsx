import * as Select from "@radix-ui/react-select";
import {
  ChevronDownIcon,
  CheckIcon,
} from "@radix-ui/react-icons";

export default function CustomSelect({
  label,
  value,
  onValueChange,
  options,
  placeholder = "Select...",
}) {
  return (
    <div className="flex flex-col gap-2">
      {label && (
        <label className="text-xs font-medium text-slate-300">
          {label}
        </label>
      )}

      <Select.Root value={value} onValueChange={onValueChange}>
        <Select.Trigger
          className="text-xs font-medium cursor-pointer text-slate-300 inline-flex h-11 w-full items-center justify-between rounded-xl bg-white/5 px-4 text-white outline-none "
        >
          <Select.Value placeholder={placeholder} />
          <Select.Icon>
            <ChevronDownIcon />
          </Select.Icon>
        </Select.Trigger>

        <Select.Portal>
          <Select.Content
            className="inline-flex overflow-hidden rounded-xl bg-[rgb(23, 27, 38)] shadow-xl"
            position="popper"
          >
            <Select.Viewport className="p-1">
              {options.map((option) => (
                <Select.Item
                  key={option.value}
                  value={option.value}
                  className="text-xs font-medium text-slate-300 cursor-pointer select-none items-center rounded-lg py-2 pl-8 pr-4 text-white outline-none hover:bg-[rgb(23, 27, 38)] data-[highlighted]:bg-[rgb(35,40,70)]"
                >
                  <Select.ItemIndicator className="absolute left-2">
                    <CheckIcon />
                  </Select.ItemIndicator>

                  <Select.ItemText>{option.label}</Select.ItemText>
                </Select.Item>
              ))}
            </Select.Viewport>
          </Select.Content>
        </Select.Portal>
      </Select.Root>
    </div>
  );
}