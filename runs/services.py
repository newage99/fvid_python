from runs.commands.Analyze1Command import Analyze1Command


def run_analyze(instance):

    try:
        arguments_dict = {
            "fvid_length": instance.fvid_length,
            "number_of_nodes": instance.number_of_nodes,
            "upload_frequency": instance.upload_frequency,
            "run_id": instance.pk,
            "number_of_analyzed_fvids": instance.number_of_analyzed_fvids
        }
        if instance.next_fvid_to_analyze:
            arguments_dict["start_fvid"] = instance.next_fvid_to_analyze

        Analyze1Command.execute(arguments_dict)

    except Exception as e:
        print(f"run_analyze exception: {str(e)}")
