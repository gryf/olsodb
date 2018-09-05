from olsodb.db import api


def main():
    api.configure({'connection': 'sqlite://'})
    api.create_schema()
    ctx = api.get_context()

    api.create_foo(ctx, 'the value')
    foo_list = api.read_foos(ctx)
    assert len(foo_list) == 1
    assert foo_list[0].value == 'the value'
    foo = api.update_foo(ctx, 'the value', 'fourtytwo')
    assert foo.value == 'fourtytwo'
    api.delete_foo(ctx, 'fourtytwo')
    assert len(api.read_foos(ctx)) == 0


if __name__ == "__main__":
    main()
